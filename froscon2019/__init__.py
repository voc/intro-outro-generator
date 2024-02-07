#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from schedulelib import *
from easing import *
import svg.path


personmap = {
}

taglinemap = {
}

# URL to Schedule-XML
scheduleUrl = 'https://programm.froscon.de/2019/schedule.xml'

# For (really) too long titles
titlemap = {
    #
}


def introFrames(args):
	xml = etree.parse('froscon2019/artwork/intro.svg').getroot()
	pathstr = xml.find(".//*[@id='animatePath']").get('d')
	frog = xml.find(".//*[@id='animatePath']").get('d')
	path = svg.path.parse_path(pathstr)

	init = path.point(0)

	frames = int(0.5*fps)
	for i in range(0, frames):
		p = path.point(i / frames) - init
		yield (
			('animatePath', 'style', 'opacity', 0),
			('date', 'style', 'opacity', 0),
		)

	frames = 3*fps
	for i in range(0, frames):
		p = path.point(i / frames) - init
		yield (
			('frog', 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),
		)

	frames = int(0.5*fps)
	for i in range(0, frames):
		yield tuple()

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('url', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
			('date', 'style', 'opacity', easeOutQuad(i, 0, 1, frames)),
		)

	frames = int(1.5*fps)
	for i in range(0, frames):
		yield (
			('url', 'style', 'opacity', 0),
			('date', 'style', 'opacity', 1),
			('bar',   'style', 'opacity', easeLinear(i, 1, -1, frames)),
			('title', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)


	# frames = 1*fps
	# for i in range(0, frames):
	# 	yield (
	# 	)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield (
			('bar',   'style', 'opacity', 0),
			('title', 'style', 'opacity', 0),
		)

def outroFrames(args):
	xml = etree.parse('froscon2019/artwork/outro.svg').getroot()
	pathstr = xml.find(".//*[@id='animatePath']").get('d')
	frog = xml.find(".//*[@id='animatePath']").get('d')
	path = svg.path.parse_path(pathstr)

	init = path.point(0)

	frames = int(0.5*fps)
	for i in range(0, frames):
		p = path.point(i / frames) - init
		yield (
			('animatePath', 'style', 'opacity', 0),
			('recordingby', 'style', 'opacity', 0),
		)

	frames = 3*fps
	for i in range(0, frames):
		p = path.point(i / frames) - init
		yield (
			('frog', 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),
		)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield tuple()

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('recordingby',   'style', 'opacity', easeLinear(i, 0, 1, frames)),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('recordingby',   'style', 'opacity', 1),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('recordingby',   'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('recordingby',   'style', 'opacity', 0),
		)

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

	render('outro.svg',
		'../outro.ts',
		outroFrames
	)

	render('pause.svg',
		'../pause.ts',
		pauseFrames
	)


def tasks(queue, args, idlist, skiplist):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['room'] not in ('HS1', 'HS3', 'HS4', 'HS5', 'HS6', 'HS7', 'HS8', 'C116'):
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

			idx=0
			for idx, person in enumerate(persons(scheduleUrl, personmap, taglinemap, event['id'])):
				queue.put(Rendertask(
					infile = 'insert.svg',
					outfile = 'event_{}_person_{}.png'.format(str(event['id']), str(person['id'])),
					parameters = {
						'$PERSON': person['person'],
						'$TAGLINE': person['tagline'],
						}
					))

				if idx > 0:
					queue.put(Rendertask(
					infile = 'insert.svg',
					outfile = 'event_{}_persons.png'.format(str(event['id'])),
					parameters = {
						'$PERSON': event['personnames'],
						'$TAGLINE': '',
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
