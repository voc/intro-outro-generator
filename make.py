#!/usr/bin/env python3
# vim: tabstop=4 shiftwidth=4 expandtab

import sys
import os
import time
import shutil
import tempfile
import threading
import multiprocessing
from threading import Thread, Lock
from queue import Queue
import renderlib
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='C3VOC Intro-Outro-Generator', usage="see help with option -h", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('projectpath', action="store", metavar='yourproject/', type=str, help='''
    Path to your project is a required argument.
    Usage: ./make.py yourproject/
    Without any further argument(s) given, your whole project will be rendered.
    ''')
parser.add_argument('--debug', action="store_true", default=False, help='''
    Run script in debug mode and just render the debug values
    given in your projects __init.py__
    This argument must not be used together with --id
    Usage: ./make.py yourproject/ --debug
    ''')
parser.add_argument('--only-frame', action="store", default=None, type=int, help='''
    Only render the given frames (of the intro), e.g. to quickly render snapshots of the tiles frame.
    Usage: ./make.py yourproject/ --debug --only-frame 300
           ./make.py yourproject/ --only-frame 300
    ''')
parser.add_argument('--id', nargs='+', action="store", type=int, help='''
    Only render the given ID(s) from your projects schedule.
    This argument must not be used together with --debug
    Usage: ./make.py yourproject/ --id 4711 0815 4223 1337
    To skip all IDs (just generate intro/outro/background files) use it with --id 000000
    ''')
parser.add_argument('--skip', nargs='+', action="store", type=str, help='''
    Skip outro, pause and/or background files in rendering if not needed.
    This argument must not be used together with --debug
    Usage: ./make.py yourproject/ --skip pause out bg
    Example - only generate outro: ./make.py yourproject/ --skip pause bg
    Example - only generate pause and background: ./make.py yourproject/ --skip out
    ''')
parser.add_argument('--skip-frames', action="store", default=None, type=int, help='''
    Skip first n frames e.g. to quickly rerender during debugging.
    Usage: ./make.py yourproject/ --debug --skip-frames 300
    ''')
parser.add_argument('--imagemagick', action="store_true", default=False, help='''
     Render frames using ImageMagick instead of Inkscape.
     Usage: ./make.py yourproject/ --imagemagick
     ''')
parser.add_argument('--gst', action="store_true", default=False, help='''
    Use gstreamer+cairo+rsvg based renderer
    ''')

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if not (args.debug is False or args.id is None):
    print("##################################################")
    print("Error! You must not use --debug and --id together!")
    print("##################################################")
    parser.print_help()
    sys.exit(1)

if not (args.debug is False or args.skip is None):
    print("####################################################")
    print("Error! You must not use --debug and --skip together!")
    print("####################################################")
    parser.print_help()
    sys.exit(1)

print(args)

# Set values from argparse
projectname = args.projectpath.strip('/')
projectpath = args.projectpath

# Check if project exists
try:
    project = renderlib.loadProject(projectname)
except ImportError:
    print("you must specify a project-name as first argument, eg. './make.py sotmeu14'. The supplied value '{0}' seems not to be a valid project (there is no '{0}/__init__.py').\n".format(projectname))
    raise

# using --debug skips the threading, the network fetching of the schedule and
# just renders one type of video
renderlib.debug = args.debug
renderlib.args = args
# sys.exit(1)


def render(infile, outfile, sequence, parameters={}, workdir=os.path.join(projectname, 'artwork')):
    task = renderlib.Rendertask(infile=infile, outfile=outfile, sequence=sequence, parameters=parameters, workdir=workdir)
    return renderlib.rendertask(task)


# debug-mode selected by --debug switch
if renderlib.debug:
    print("!!! DEBUG MODE !!!")

    # expose debug-render method
    project.render = render

    # call into project which calls render as needed
    project.debug()

    # exit early
    sys.exit(0)

# threaded task queue
tasks = Queue()

# initialize args.id and args.skip, if they are not given by the user
if (args.id is None):
    args.id = []

if (args.skip is None):
    args.skip = []

# call into project which generates the tasks
project.tasks(tasks, projectpath, args.id, args.skip)

# one working thread per cpu
num_worker_threads = multiprocessing.cpu_count()
print("{0} tasks in queue, starting {1} worker threads".format(tasks.qsize(), num_worker_threads))

# put a sentinel for each thread into the queue to signal the end
for _ in range(num_worker_threads):
    tasks.put(None)

# this lock ensures, that only one thread at a time is writing to stdout
# and avoids output from multiple threads intermixing
printLock = Lock()


def tprint(str):
    # aquire lock
    printLock.acquire()

    # print thread-name and message
    print(threading.current_thread().name + ': ' + str)

    # release lock
    printLock.release()


# thread worker
def worker():
    # generate a tempdir for this worker-thread and use the artwork-subdir as temporary folder
    tempdir = tempfile.mkdtemp()
    workdir = os.path.join(tempdir, 'artwork')

    # save the current working dir as output-dir
    outdir = os.path.join(os.getcwd(), projectname)

    # print a message that we're about to initialize our environment
    tprint("initializing worker in {0}, writing result to {1}".format(tempdir, outdir))

    # copy the artwork-dir into the tempdir
    shutil.copytree(os.path.join(projectname, 'artwork'), workdir)

    # loop until all tasks are done (when the thread fetches a sentinal from the queue)
    while True:
        # fetch a task from the queue
        task = renderlib.Rendertask.ensure(tasks.get())

        # if it is a stop-sentinal break out of the loop
        if task is None:
            break

        # print that we're about to render a task
        tprint('rendering {0} from {1}'.format(task.outfile, task.infile))

        # prepend workdir to input file
        task.infile = os.path.join(workdir, task.infile)
        task.outfile = os.path.join(outdir, task.outfile)
        task.workdir = workdir

        # render with these arguments
        renderlib.rendertask(task)

        # print that we're finished
        tprint('finished {0}, {1} tasks left'.format(task.outfile, max(0, tasks.qsize() - num_worker_threads)))

        # mark the task as finished
        tasks.task_done()

    # all tasks from the queue done, clean up
    tprint("cleaning up worker")

    # remove the tempdir
    shutil.rmtree(tempdir)

    # mark the sentinal as done
    tasks.task_done()


# List of running threads
threads = []

# generate and start the threads
for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()
    threads.append(t)

# wait until they finished doing the work
# we're doing it the manual way because tasks.join() would wait until all tasks are done,
# even if the worker threads crash due to broken svgs, Ctrl-C termination or whatnot
while True:
    if tasks.empty() is True:
        break

    # sleep while the workers work
    time.sleep(1)

print("all worker threads ended")
