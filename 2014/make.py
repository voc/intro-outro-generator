#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import glob
import os
import re
import shutil
import errno
import unicodedata
import urllib2
#import xml.etree.ElementTree as etree
from lxml import etree
import cssutils
import textwrap
import tempfile
import threading
import multiprocessing
from threading import Thread, Lock
from Queue import Queue

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

# t: current time, b: begInnIng value, c: change In value, d: duration
# copied from jqueryui
def easeOutCubic(t, b, c, d):
	t=float(t)/d-1
	return c*((t)*t*t + 1) + b

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

# Normalizes string, converts to lowercase, removes non-alpha characters,
 #and converts spaces to hyphens.
def slugify(value):
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
	value = unicode(re.sub('[-\s]+', '-', value))
	return value

# create a filename from the events' id and a slugified version of the title
def vorspannFilename(id, title):
	return u'{0:04d}-{1}.dv'.format(id, slugify(unicode(title)))

# svg does not have a method for automatic line breaking, that rsvg is capable of
# so we do it in python as good as we can
def vorspannTitle(title):
	return '</tspan><tspan x="150" dy="45">'.join(textwrap.wrap(title, 35))

def vorspannUrl(id):
	return 'fossgis.de/konferenz/2014/programm/events/'+str(id)+'.de.html'


def abspannFrames():
	# 5 Sekunden

	# 2 Sekunden Fadein Text
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('banderole', 'opacity', "%.2f" % easeOutCubic(i, 0, 1, frames) ),
			('license', 'opacity', 0)
		}

	# 2 Sekunde Fadein Lizenz-Logo
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('banderole', 'opacity', 1),
			('license', 'opacity', "%.2f" % (float(i)/frames))
		}

	# 1 Sekunde stehen bleiben
	frames = 1*fps
	for i in range(0, frames):
		yield {
			('banderole', 'opacity', 1),
			('license', 'opacity', 1)
		}

def vorspannFrames():
	# 7 Sekunden

	# 2 Sekunden Text 1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box',   'opacity', "%.2f" % easeOutCubic(i, 0, 1, frames)),
			('text1', 'opacity', "%.2f" % easeOutCubic(i, 0, 1, frames)),
			('text2', 'opacity', 0)
		)

	# 1 Sekunde Fadeout Text 1
	frames = 1*fps
	for i in range(0, frames):
		yield {
			('box',   'opacity', 1),
			('text1', 'opacity', "%.2f" % (1-(float(i)/frames))),
			('text2', 'opacity', 0)
		}

	# 2 Sekunden Text 2
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('box',   'opacity', 1),
			('text1', 'opacity', 0),
			('text2', 'opacity', "%.2f" % easeOutCubic(i, 0, 1, frames))
		}

	# 2 Sekunden stehen bleiben
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('box',   'opacity', 1),
			('text1', 'opacity', 0),
			('text2', 'opacity', 1)
		}

def pauseFrames():
	# 12 Sekunden

	# 2 Sekunden Text1 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('text1', 'opacity', 1),
			('text2', 'opacity', 0)
		}

	# 2 Sekunden Fadeout Text1
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('text1', 'opacity', "%.2f" % (1-easeOutCubic(i, 0, 1, frames))),
			('text2', 'opacity', 0)
		}

	# 2 Sekunden Fadein Text2
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('text1', 'opacity', 0),
			('text2', 'opacity', "%.2f" % easeOutCubic(i, 0, 1, frames))
		}

	# 2 Sekunden Text2 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('text1', 'opacity', 0),
			('text2', 'opacity', 1)
		}

	# 2 Sekunden Fadeout Text2
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('text1', 'opacity', 0),
			('text2', 'opacity', "%.2f" % (1-easeOutCubic(i, 0, 1, frames)))
		}

	# 2 Sekunden Fadein Text1
	frames = 2*fps
	for i in range(0, frames):
		yield {
			('text1', 'opacity', "%.2f" % (easeOutCubic(i, 0, 1, frames))),
			('text2', 'opacity', 0)
		}

cssutils.ser.prefs.lineSeparator = ' '

def render(infile, outfile, sequence, parameters={}, workdir='artwork'):
	# in debug mode we have no thread-worker which prints its progress
	if debug:
		print "generating {0} from {1}".format(outfile, infile)

	# make sure a .frames-directory exists in out workdir
	ensurePathExists(os.path.join(workdir, '.frames'))

	# open and parse the input file
	with open(os.path.join(workdir, infile), 'r') as fp:
		svgstr = fp.read()
		for key in parameters.keys():
			svgstr = svgstr.replace(key, str(parameters[key]))

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
				(id, key, value) = replaceinfo

				for el in svg.findall(".//*[@id='"+id.replace("'", "\\'")+"']"):
					style = cssutils.parseStyle( el.attrib['style'] )
					style[key] = unicode(value)
					el.attrib['style'] = style.cssText

			# write the generated svg-text into the output-file
			fp.write( etree.tostring(svg) )

		# invoke rsvg to convert the generated svg-file into a png inside the .frames-directory
		os.system('cd {0} && rsvg-convert .gen.svg > .frames/{1:04d}.png'.format(workdir, frameNr))

		# incrwement frame-number
		frameNr += 1

	# remove the dv we are about to (re-)generate
	ensureFilesRemoved(os.path.join(workdir, outfile))

	# invoke avconv aka ffmpeg and renerate a lossles-dv from the frames
	#  if we're not in debug-mode, suppress all output
	os.system('cd {0} && avconv -ar 48000 -ac 2 -f s16le -i /dev/zero -f image2 -i .frames/%04d.png -target pal-dv -shortest "{1}"'.format(workdir, outfile) + ('' if debug else '>/dev/null 2>&1'))

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
		response = urllib2.urlopen('http://www.fossgis.de/konferenz/2014/programm/schedule.de.xml')

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
				yield ( int(event.get('id')), event.find('title').text, ', '.join(personnames) )


# debug-mode selected by --debug switch
if debug:
	print "!!! DEBUG MODE !!!"
	title = 'OpenJUMP - Überblick, Neuigkeiten, Zusammenarbeit/Schnittstellen mit proprietärer Software'

	render(
		'vorspann.svg',
		os.path.join('..', str(667)+".dv"),
		vorspannFrames,
		{
			'$id': 667,
			'$title': vorspannTitle(title),
			'$personnames': 'Matthias Scholz'
		}
	)

	render(
		'abspann.svg',
		'../outro.dv',
		abspannFrames
	)

	render('pause.svg',
		'../pause.dv',
		pauseFrames
	)

	sys.exit(0)



# threaded task queue
tasks = Queue()

titlemap = {
	708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}

# iterate over all events extracted from the schedule xml-export
for (id, title, personnames) in events():
	if id in titlemap:
		title = titlemap[id]

	# generate a task description and put them into the queue
	tasks.put((
		'vorspann.svg',
		str(id)+".dv",
		vorspannFrames,
		{
			'$id': id,
			'$title': vorspannTitle(title),
			'$personnames': personnames
		}
	))

# place a task for the outro into the queue
tasks.put((
	'abspann.svg',
	'outro.dv',
	abspannFrames
))

# place the pause-sequence into the queue
tasks.put((
	'pause.svg',
	'pause.dv',
	pauseFrames
))

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
	outdir = os.getcwd()

	# print a message that we're about to initialize our environment
	tprint("initializing worker in {0}, writing result to {1}".format(tempdir, outdir))

	# copy the artwork-dir into the tempdir
	shutil.copytree('artwork', workdir)

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


# generate and start the threads
for i in range(num_worker_threads):
	t = Thread(target=worker)
	t.daemon = True
	t.start()

# wait until they finished doing the work
tasks.join()
print "all worker threads ended"
