#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from schedulelib import *
from easing import *
import svg.path

# URL to Schedule-XML
scheduleUrl = 'https://programm.froscon.org/2025/schedule.xml'

# For (really) too long titles
titlemap = {
    #
}


def introFrames(args):
	xml = etree.parse('froscon2025/artwork/intro.svg').getroot()
	pathstr = xml.find(".//*[@id='animatePath']").get('d')
	frog = xml.find(".//*[@id='animatePath']").get('d')
	path = svg.path.parse_path(pathstr)

	init = path.point(0)

	frames = 3*fps
	for i in range(0, frames):
		p = path.point(i / frames) - init
		yield (
			('animatePath', 'style', 'opacity', 0),
			('frog',  'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag+120)),
			('title', 'style', 'opacity', 0),
			('names', 'style', 'opacity', 0),
		)

#	frames = int(0.5*fps)
#	for i in range(0, frames):
#		yield (
#			('animatePath', 'style', 'opacity', 0),
#			('frog',  'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag+120)),
#			('title',   'style', 'opacity', easeLinear(i, 0, 1, frames)),
#			('names', 'style', 'opacity', easeLinear(i, 0, 1, frames)),
#		)

	frames = int(3.0*fps)
	for i in range(0, frames):
		yield (
			('animatePath', 'style', 'opacity', 0),
			('frog',  'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag+120)),
		)

def outroFrames(args):
	xml = etree.parse('froscon2025/artwork/outro.svg').getroot()

	frames = int(4*fps)
	for i in range(0, frames):
		yield ()

def pauseFrames(args):
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 1),
			('text2', 'style', 'opacity', 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
			('text2', 'style', 'opacity', 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', easeLinear(i, 0, 1, frames)),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', 1),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', easeLinear(i, 0, 1, frames)),
			('text2', 'style', 'opacity', 0),
		)

def debug():
	render('intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': 2404,
			'$title': 'Linux Container im High Performance Computing',
			'$subtitle': 'Vom Wal zur Singularität und weiter',
			'$personnames': 'Holger Gantikow'
		}
	)

#	render('outro.svg',
#		'../outro.ts',
#		outroFrames
#	)

#	render('pause.svg',
#		'../pause.ts',
#		pauseFrames
#	)


def tasks(queue, args, idlist, skiplist):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['room'] not in ('HS 1/2', 'HS 3', 'HS 4', 'HS 5', 'HS 6', 'HS 7', 'HS 8'):
			print("skipping room %s (%s)" % (event['room'], event['title']))
			continue

		if (event['id'] in idlist or not idlist) and not 'intro' in skiplist:
		# generate a task description and put them into the queue
			queue.put(Rendertask(
				infile = 'intro.svg',
				outfile = str(event['id'])+".ts",
				sequence = introFrames,
				parameters = {
					'$id': event['id'],
					'$title': event['title'],
#					'$subtitle': event['subtitle'],
					'$personnames': event['personnames']
				}
			))

	if not 'outro' in skiplist:
		# place a task for the outro into the queue
		queue.put(Rendertask(
			infile = 'outro.svg',
			outfile = 'outro.ts',
			sequence = outroFrames
		))

	if not 'pause' in skiplist:
		# place the pause-sequence into the queue
		queue.put(Rendertask(
			infile = 'pause.svg',
			outfile = 'pause.ts',
			sequence = pauseFrames
		))
