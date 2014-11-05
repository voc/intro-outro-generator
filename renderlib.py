#!/usr/bin/python3

import os
import sys
import glob
import math
import shutil
import errno
from lxml import etree
from xml.sax.saxutils import escape as xmlescape
import cssutils
import logging
import subprocess
from urllib.request import urlopen

# Frames per second. Increasing this renders more frames, the avconf-statements would still need modifications
fps = 25
debug = False

cssutils.ser.prefs.lineSeparator = ' '
cssutils.log.setLevel(logging.FATAL)

def loadProject(projectname):
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), projectname))
	return __import__(projectname)

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

def easeInOutQuad(t, b, c, d):
	t=float(t)/(d/2)
	if (t < 1):
		return c/2*t*t + b;
	t=t-1
	return -c/2 * (t*(t-2) - 1) + b;

def easeLinear(t, b, c, d):
	t=float(t)/d
	return t*c+b

class Rendertask:
	def __init__(self, infile, sequence, parameters={}, outfile=None, workdir='.'):
		self.infile =  infile
		self.sequence = sequence
		self.parameters = parameters
		self.outfile = outfile
		self.workdir = workdir

	def fromtupel(tuple):
		return Rendertask(tuple[0], tuple[2], tuple[3], tuple[1])

	def ensure(input):
		if isinstance(input, tuple):
			return Rendertask.fromtupel(input)
		elif isinstance(input, Rendertask):
			return input
		else:
			return None

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

def rendertask(task):
	# in debug mode we have no thread-worker which prints its progress
	if debug:
		print("generating {0} from {1}".format(task.outfile, task.infile))

	# make sure a .frames-directory exists in out workdir
	ensurePathExists(os.path.join(task.workdir, '.frames'))

	# open and parse the input file
	with open(os.path.join(task.workdir, task.infile), 'r') as fp:
		svgstr = fp.read()
		for key in task.parameters.keys():
			svgstr = svgstr.replace(key, xmlescape(str(task.parameters[key])))

		svg = etree.fromstring(svgstr.encode('utf-8'))

	# frame-number counter
	frameNr = 0

	# iterate through the animation seqence frame by frame
	# frame is a ... tbd
	for frame in task.sequence(task.parameters):
		# print a line for each and every frame generated
		if debug:
			print("frameNr {0:3d} => {1}".format(frameNr, frame))

		# open the output-file (named ".gen.svg" in the workdir)
		with open(os.path.join(task.workdir, '.gen.svg'), 'w') as fp:
			# apply the replace-pairs to the input text, by finding the specified xml-elements by thier id and modify thier css-parameter the correct value
			for replaceinfo in frame:
				(id, type, key, value) = replaceinfo

				for el in svg.findall(".//*[@id='"+id.replace("'", "\\'")+"']"):
					if type == 'style':
						style = cssutils.parseStyle( el.attrib['style'] if 'style' in el.attrib else '' )
						style[key] = str(value)
						el.attrib['style'] = style.cssText

					elif type == 'attr':
						el.attrib[key] = str(value)

					elif type == 'text':
						el.text = str(value)

			# write the generated svg-text into the output-file
			fp.write( etree.tostring(svg, encoding='unicode') )

		# invoke inkscape to convert the generated svg-file into a png inside the .frames-directory
		errorReturn = subprocess.check_output('cd {0} && inkscape --export-background=white --export-png=.frames/{1:04d}.png .gen.svg 2>&1 >/dev/null'.format(task.workdir, frameNr), shell=True, universal_newlines=True)
		if errorReturn != '':
			print("inkscape exitted with error\n"+errorReturn)
			sys.exit(42)

		# increment frame-number
		frameNr += 1



	# remove the dv we are about to (re-)generate
	ensureFilesRemoved(os.path.join(task.workdir, task.outfile))

	# invoke avconv aka ffmpeg and renerate a lossles-dv from the frames
	#  if we're not in debug-mode, suppress all output
	os.system('cd {0} && ffmpeg -ar 48000 -ac 2 -f s16le -i /dev/zero -f image2 -i .frames/%04d.png -target pal-dv -aspect 16:9 -shortest "{1}"'.format(task.workdir, task.outfile) + ('' if debug else '>/dev/null 2>&1'))

	# as before, in non-debug-mode the thread-worker does all progress messages
	if debug:
		print("cleanup")

	# remove the .frames-dir with all frames in it
	shutil.rmtree(os.path.join(task.workdir, '.frames'))

	# remove the generated svg
	ensureFilesRemoved(os.path.join(task.workdir, '.gen.svg'))


# Download the Events-Schedule and parse all Events out of it. Yield a tupel for each Event
def events(scheduleUrl, titlemap={}):
	print("downloading pentabarf schedule")

	# download the schedule
	response = urlopen(scheduleUrl)

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
				if event.find('persons') is not None:
					for person in event.find('persons').iter('person'):
						personnames.append(person.text)

				# yield a tupel with the event-id, event-title and person-names
				yield {
					'id': int(event.get('id')),
					'title': titlemap[id] if id in titlemap else event.find('title').text,
					'subtitle': event.find('subtitle').text if event.find('subtitle') is not None else '',
					'persons': personnames,
					'personnames': ', '.join(personnames)
				}

try:
	from termcolor import colored
except ImportError:
	def colored(str, col):
		return str
