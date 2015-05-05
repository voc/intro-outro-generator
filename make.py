#!/usr/bin/env python3

import sys
import os
import time
import shutil
from lxml import etree
import tempfile
import threading
import multiprocessing
from threading import Thread, Lock
from queue import Queue
import renderlib

# Project-Name
if len(sys.argv) < 2:
	print("you must specify a project-name as first argument, eg. './make.py sotmeu14'")
	sys.exit(1)

args = sys.argv[1:]

projectname = args.pop(0).strip('/')
try:
	project = renderlib.loadProject(projectname)
except ImportError:
	print("you must specify a project-name as first argument, eg. './make.py sotmeu14'. The supplied value '{0}' seems not to be a valid project (there is no '{0}/__init__.py').\n".format(projectname))
	raise

# using --debug skips the threading, the network fetching of the schedule and
# just renders one type of video
renderlib.debug = ('--debug' in sys.argv)

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

# call into project which generates the tasks
project.tasks(tasks, args)

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
	print(threading.current_thread().name+': '+str)

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
		if task == None:
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
	if tasks.empty() == True:
		break

	# sleep while the workers work
	time.sleep(1)

print("all worker threads ended")
