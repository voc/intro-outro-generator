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

# Frames per second. Increasing this renders more frames, the avconf-statements would still need modifications
fps = 25

# using --debug skips the threading, the network fetching of the schedule and
# just renders one type of video
debug = ('--debug' in sys.argv)

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

def pauseFrames():
	# 7 Sekunden

	frames = 7*fps
	for i in range(0, frames):
		yield (
			('sun', 'attr',	'transform', "translate(625, 625) translate(-450, -375) rotate(%.4f) translate(-625, -625)" % (float(i)/float(frames)*30)),
		)


cssutils.ser.prefs.lineSeparator = ' '
cssutils.log.setLevel(logging.ERROR)

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


render(
	'pause.svg',
	'../pause.dv',
	pauseFrames
)

render(
	'novideo.svg',
	'../novideo.dv',
	pauseFrames
)

render(
	'nostream.svg',
	'../nostream.dv',
	pauseFrames
)
