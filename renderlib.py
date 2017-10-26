#!/usr/bin/python3

import os
import sys
import re
import glob
import math
import shutil
import errno
import shutil
from lxml import etree
from xml.sax.saxutils import escape as xmlescape
import cssutils
import logging
import subprocess
from urllib.request import urlopen

# Frames per second. Increasing this renders more frames, the avconf-statements would still need modifications
fps = 25
debug = False
args = None

cssutils.ser.prefs.lineSeparator = ' '
cssutils.log.setLevel(logging.FATAL)

def loadProject(projectname):
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), projectname))
	return __import__(projectname)

def easeDelay(easer, delay, t, b, c, d, *args):
	if t < delay:
		return b

	if t - delay > d:
		return b+c

	return easer(t - delay, b, c, d, *args)

class Rendertask:
	def __init__(self, infile, sequence, parameters={}, outfile=None, workdir='.'):
		if isinstance(infile, list):
			self.infile =  infile[0]
			self.audiofile = infile[1]
		else:
			self.infile =  infile
			self.audiofile = None
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
	global args
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

		parser = etree.XMLParser(huge_tree=True)
		svg = etree.fromstring(svgstr.encode('utf-8'), parser)

	# frame-number counter
	frameNr = 0

	# iterate through the animation seqence frame by frame
	# frame is a ... tbd
	cache = {}
	for frame in task.sequence(task.parameters):
		skip_rendering = False
		# skip first n frames, to speed up rerendering during debugging
		if 'only_rerender_frames_after' in task.parameters:
			skip_rendering = (frameNr <= task.parameters['only_rerender_frames_after'])
		
		if args.skip_frames:
			skip_rendering = (frameNr <= args.skip_frames)
		
		if args.only_frame:
			skip_rendering = (frameNr != args.only_frame)
		
		# print a line for each and every frame generated
		if debug and not skip_rendering:
			print("frameNr {0:3d} => {1}".format(frameNr, frame))

		frame = tuple(frame)
		if frame in cache:
			if debug:
				print("cache hit, reusing frame {0}".format(cache[frame]))

			framedir = task.workdir + "/.frames/"
			shutil.copyfile("{0}/{1:04d}.png".format(framedir, cache[frame]), "{0}/{1:04d}.png".format(framedir, frameNr))

			frameNr += 1
			continue
		else:
			cache[frame] = frameNr

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

		if not skip_rendering:
			# open the output-file (named ".gen.svg" in the workdir)
			with open(os.path.join(task.workdir, '.gen.svg'), 'w') as fp:
				# write the generated svg-text into the output-file
				fp.write( etree.tostring(svg, encoding='unicode') )
	
			if task.outfile.endswith('.ts'):
				width = 1920
				height = 1080
			else:
				width = 1024
				height = 576
	
			# invoke inkscape to convert the generated svg-file into a png inside the .frames-directory
			cmd = 'cd {0} && inkscape --export-background=white --export-width={2} --export-height={3} --export-png=$(pwd)/.frames/{1:04d}.png $(pwd)/.gen.svg 2>&1 >/dev/null'.format(task.workdir, frameNr, width, height)
			errorReturn = subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
			if errorReturn != '':
				print("inkscape exitted with error\n"+errorReturn)
				sys.exit(42)

		# increment frame-number
		frameNr += 1



	if args.only_frame:
		task.outfile = '{0}.frame{1:04d}.png'.format(task.outfile, args.only_frame)


	# remove the dv/ts we are about to (re-)generate
	ensureFilesRemoved(os.path.join(task.workdir, task.outfile))

	if task.outfile.endswith('.png'):
		cmd = 'cd {0} && cp ".frames/{1:04d}.png" "{2}"'.format(task.workdir, args.only_frame, task.outfile)

	# invoke avconv aka ffmpeg and renerate a lossles-dv from the frames
	#  if we're not in debug-mode, suppress all output
	elif task.outfile.endswith('.ts'):
		cmd = 'cd {0} && '.format(task.workdir)
		cmd += 'ffmpeg -f image2 -i .frames/%04d.png '
		if task.audiofile is None:
			cmd += '-ar 48000 -ac 1 -f s16le -i /dev/zero -ar 48000 -ac 1 -f s16le -i /dev/zero '
		else:
			cmd += '-i {0} -i {0} '.format(task.audiofile)

		cmd += '-map 0:0 -c:v mpeg2video -q:v 5 -aspect 16:9 '

		if task.audiofile is None:
			cmd += '-map 1:0 -map 2:0 '
		else:
			cmd += '-map 1:0 -c:a copy -map 2:0 -c:a copy '
		cmd += '-shortest -f mpegts "{0}"'.format(task.outfile)
	else:
		cmd = 'cd {0} && ffmpeg -ar 48000 -ac 2 -f s16le -i /dev/zero -f image2 -i .frames/%04d.png -target pal-dv -aspect 16:9 -shortest "{1}"'.format(task.workdir, task.outfile)

	if debug:
		print(cmd)

	r = os.system(cmd + ('' if debug else '>/dev/null 2>&1'))

	# as before, in non-debug-mode the thread-worker does all progress messages
	if debug:
		if r != 0:
			sys.exit()

	if not debug:
		print("cleanup")


		# remove the generated svg
		ensureFilesRemoved(os.path.join(task.workdir, '.gen.svg'))


# Download the Events-Schedule and parse all Events out of it. Yield a tupel for each Event
def events(scheduleUrl, titlemap={}):
	print("downloading schedule")

	# download the schedule
	response = urlopen(scheduleUrl)

	# read xml-source
	xml = response.read()

	# parse into ElementTree
	parser = etree.XMLParser(huge_tree=True)
	schedule = etree.fromstring(xml, parser)

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
						personname = re.sub( '\s+', ' ', person.text ).strip()
						personnames.append(personname)

				id = int(event.get('id'))

				if id in titlemap:
					title = titlemap[id]
				elif event.find('title') is not None and event.find('title').text is not None:
					title = re.sub( '\s+', ' ', event.find('title').text ).strip()
				else:
					title = ''

				if event.find('subtitle') is not None and event.find('subtitle').text is not None:
					subtitle = re.sub( '\s+', ' ', event.find('subtitle').text ).strip()
				else:
					subtitle = ''

				# yield a tupel with the event-id, event-title and person-names
				yield {
					'id': id,
					'title': title,
					'subtitle': subtitle,
					'persons': personnames,
					'personnames': ', '.join(personnames),
					'room': room.attrib['name'],
				}

try:
	from termcolor import colored
except ImportError:
	def colored(str, col):
		return str
