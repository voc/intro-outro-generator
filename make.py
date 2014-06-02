#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import glob
import os
import re
import math
import time
import shutil
import errno
import urllib2
from lxml import etree
from xml.sax.saxutils import escape as xmlescape
import cssutils
import logging
import tempfile
import threading
import multiprocessing
from threading import Thread, Lock
import subprocess
from Queue import Queue

# Project-Name
if len(sys.argv) < 2:
	print "you must specify a project-name as first argument, eg. './make.py sotmeu14'"
	sys.exit(1)

projectname = sys.argv[1].strip('/')
try:
	sys.path.append(projectname)
	project = __import__(projectname)
except ImportError:
	print "you must specify a project-name as first argument, eg. './make.py sotmeu14'. The supplied value '{0}' seems not to be a valid project (there is no '{0}/__init__.py').".format(projectname);
	sys.exit(1)

# Frames per second. Increasing this renders more frames, the avconf-statements would still need modifications
fps = 25

# using --debug skips the threading, the network fetching of the schedule and
# just renders one type of video
debug = ('--debug' in sys.argv)

# using --offline only skips the network fetching and use a local schedule.de.xml
offline = ('--offline' in sys.argv)

# set charset of output-terminal
reload(sys)
sys.setdefaultencoding('utf-8')

# try to create all folders needed and skip, they already exist
def ensurePathExists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

# remove the files matched by the pattern
def ensureFilesRemoved(pattern):
	for f in glob.glob(pattern):
		os.unlink(f)

cssutils.ser.prefs.lineSeparator = ' '
cssutils.log.setLevel(logging.ERROR)

def render(infile, outfile, sequence, parameters={}, workdir=os.path.join(projectname, 'artwork')):
	# in debug mode we have no thread-worker which prints its progress
	if debug:
		print "generating {0} from {1}".format(outfile, infile)

	# make sure a .frames-directory exists in out workdir
	ensurePathExists(os.path.join(workdir, '.frames'))

	# open and parse the input file
	with open(os.path.join(workdir, infile), 'r') as fp:
		svgstr = fp.read()
		for key in parameters.keys():
			svgstr = svgstr.replace(key, xmlescape(str(parameters[key])))

		svg = etree.fromstring(svgstr)

	# find all images and force them to absolute file-urls
	namespaces = {'xlink': 'http://www.w3.org/1999/xlink', 'svg': 'http://www.w3.org/2000/svg'}
	for el in svg.findall(".//svg:image[@xlink:href]", namespaces=namespaces):
		el.attrib['{http://www.w3.org/1999/xlink}href'] = 'file:///' + os.path.realpath(workdir) + '/' + el.attrib['{http://www.w3.org/1999/xlink}href']

	# frame-number counter
	frameNr = 0

	# iterate through the animation seqence frame by frame
	# frame is a ... tbd
	for frame in sequence():
		# print a line for each and every frame generated
		if debug:
			print "frameNr {0:2d} => {1}".format(frameNr, frame)

		# open the output-file (named ".gen.svg" in the workdir)
		with open(os.path.join(workdir, '.gen.svg'), 'w') as fp:
			# apply the replace-pairs to the input text, by finding the specified xml-elements by thier id and modify thier css-parameter the correct value
			for replaceinfo in frame:
				(id, type, key, value) = replaceinfo

				for el in svg.findall(".//*[@id='"+id.replace("'", "\\'")+"']"):
					if type == 'style':
						style = cssutils.parseStyle( el.attrib['style'] if 'style' in el.attrib else '' )
						style[key] = unicode(value)
						el.attrib['style'] = style.cssText

					elif type == 'attr':
						el.attrib[key] = value

			# write the generated svg-text into the output-file
			fp.write( etree.tostring(svg) )

		# invoke inkscape to convert the generated svg-file into a png inside the .frames-directory
		errorReturn = subprocess.check_output('cd {0} && inkscape --export-png=.frames/{1:04d}.png .gen.svg 2>&1 >/dev/null'.format(workdir, frameNr), shell=True)
		if errorReturn != '':
			print "inkscape exitted with error\n"+errorReturn
			sys.exit(42)

		# increment frame-number
		frameNr += 1



	# remove the dv we are about to (re-)generate
	ensureFilesRemoved(os.path.join(workdir, outfile))

	# invoke avconv aka ffmpeg and renerate a lossles-dv from the frames
	#  if we're not in debug-mode, suppress all output
	os.system('cd {0} && ffmpeg -ar 48000 -ac 2 -f s16le -i /dev/zero -f image2 -i .frames/%04d.png -target pal-dv -aspect 16:9 -shortest "{1}"'.format(workdir, outfile) + ('' if debug else '>/dev/null 2>&1'))

	# as before, in non-debug-mode the thread-worker does all progress messages
	if debug:
		print "cleanup"

	# remove the .frames-dir with all frames in it
	shutil.rmtree(os.path.join(workdir, '.frames'))

	# remove the generated svg
	ensureFilesRemoved(os.path.join(workdir, '.gen.svg'))



# Download the Events-Schedule and parse all Events out of it. Yield a tupel for each Event
def events():
	print "downloading pentabarf schedule"

	# use --offline to skip networking
	if offline:
		# parse the offline-version
		schedule = etree.parse('schedule.de.xml').getroot()

	else:
		# download the schedule
		response = urllib2.urlopen(project.scheduleUrl)

		# read xml-source
		xml = response.read()

		# parse into ElementTree
		schedule = etree.fromstring(xml)

	# iterate all days
	for day in schedule.iter('day'):
		# iterate all rooms
		for room in day.iter('room'):
			# iterate events on that day in this room
			for event in room.iter('event'):
				# aggregate names of the persons holding this talk
				personnames = []
				for person in event.find('persons').iter('person'):
					personnames.append(person.text)

				# yield a tupel with the event-id, event-title and person-names
				yield {
					'id': int(event.get('id')),
					'title': project.titlemap[id] if id in project.titlemap else event.find('title').text,
					'subtitle': event.find('subtitle').text or '',
					'persons': personnames,
					'personnames': ', '.join(personnames)
				}

# expose helper-methods method to project
project.events = events
project.render = render

project.fps = fps

# t: current time, b: begInnIng value, c: change In value, d: duration
# copied from jqueryui
def easeOutCubic(t, b, c, d):
	t=float(t)/d-1
	return c*((t)*t*t + 1) + b

def easeInCubic(t, b, c, d):
	t=float(t)/d
	return c*(t)*t*t + b;

def easeOutQuad(t, b, c, d):
	t=float(t)/d
	return -c *(t)*(t-2) + b;

# expose easings to project
project.easeOutCubic = easeOutCubic
project.easeInCubic = easeInCubic
project.easeOutQuad = easeOutQuad

# debug-mode selected by --debug switch
if debug:
	print "!!! DEBUG MODE !!!"

	# call into project which calls render as needed
	project.debug()

	# exit early
	sys.exit(0)



# threaded task queue
tasks = Queue()

# call into project which generates the tasks
project.tasks(tasks)

# one working thread per cpu
num_worker_threads = multiprocessing.cpu_count()
print "{0} tasks in queue, starting {1} worker threads".format(tasks.qsize(), num_worker_threads)

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
	print threading.current_thread().name+': '+str

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
		task = tasks.get()

		# if it is a stop-sentinal break out of the loop
		if task == None:
			break

		# print that we're about to render a task
		tprint('rendering {0}'.format(task[1]))

		# render options
		opts = (
			# argument 0 is the input file. prepend the workdir
			os.path.join(workdir, task[0]),

			# argument 1 is the output file. prepend the outdir
			os.path.join(outdir, task[1]),

			# argument 2 is the frame generator, nothing to do here
			task[2],

			# argument 3 are the extra parameters
			task[3] if len(task) > 3 else {},

			# argument 4 is the workdir path
			workdir
		)

		# render with these arguments
		render(*opts)

		# print that we're finished
		tprint('finished {0}, {1} tasks left'.format(task[1], max(0, tasks.qsize() - num_worker_threads)))

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

print "all worker threads ended"
