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
import datetime



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
    outdir = projectpath + "/output"

    # print a message that we're about to initialize our environment
    tprint("initializing worker in {0}, writing result to {1}".format(tempdir, outdir))

    # copy the artwork-dir into the tempdir
    shutil.copytree(projectpath + '/artwork', workdir)

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
        with open(f"{projectpath}/tasks_left", "a") as file:
            file.write(f"{tasks.qsize()} {datetime.datetime.now()}\n")
        tprint('finished {0}, {1} tasks left'.format(task.outfile, max(0, tasks.qsize() - num_worker_threads)))

        # mark the task as finished
        tasks.task_done()

    # all tasks from the queue done, clean up
    tprint("cleaning up worker")

    # remove the tempdir
    shutil.rmtree(tempdir)

    # mark the sentinal as done
    tasks.task_done()


def main(path, schedule, ids = []):
    global projectpath
    projectpath = path
    project = renderlib.loadProject()
    project.scheduleUrl = schedule
    # using --debug skips the threading, the network fetching of the schedule and
    # just renders one type of video
    renderlib.args = None
    # sys.exit(1)


    # threaded task queue
    global tasks
    tasks = Queue()

    # initialize args.id and args.skip, if they are not given by the user
    skip = []

    # call into project which generates the tasks
    project.tasks(tasks, projectpath, ids, skip)

    # one working thread per cpu
    global num_worker_threads
    num_worker_threads = multiprocessing.cpu_count()
    print(f"{tasks.qsize()} tasks in queue, starting {num_worker_threads} worker threads")

    # put a sentinel for each thread into the queue to signal the end
    for _ in range(num_worker_threads):
        tasks.put(None)

    # this lock ensures, that only one thread at a time is writing to stdout
    # and avoids output from multiple threads intermixing
    global printLock 
    printLock = Lock()

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
if __name__ == "__main__":
    main("/tmp/tmpih_b_mfh")
