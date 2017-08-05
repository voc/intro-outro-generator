#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from easing import *
import svg.path

# URL to Schedule-XML
scheduleUrl = 'https://programm.froscon.de/2017/schedule.xml'

# For (really) too long titles
titlemap = {
    #
}


def introFrames(args):
	xml = etree.parse('froscon2017/artwork/intro.svg').getroot()
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
	xml = etree.parse('froscon2017/artwork/outro.svg').getroot()
	pathstr = xml.find(".//*[@id='animatePath']").get('d')
	frog = xml.find(".//*[@id='animatePath']").get('d')
	path = svg.path.parse_path(pathstr)

	init = path.point(0)

	frames = int(0.5*fps)
	for i in range(0, frames):
		p = path.point(i / frames) - init
		yield (
			('animatePath', 'style', 'opacity', 0),
			('license', 'style', 'opacity', 0),
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
			('license',   'style', 'opacity', easeLinear(i, 0, 1, frames)),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('license',   'style', 'opacity', 1),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('license',   'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style', 'opacity', 0),
			('license',   'style', 'opacity', 0),
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
			'$id': 1302,
			'$title': 'VlizedLab - Eine Open Source-Virtualisierungslösung für PC-Räume',
			'$subtitle': 'IT Automatisierung und zentrales Management mit SALT',
			'$personnames': 'Thorsten Kramm'
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


def tasks(queue, args):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['room'] not in ('Saal 1', 'Saal 3', 'Saal 4', 'Saal 5', 'Saal 6', 'Saal 7', 'Saal 8'):
			print("skipping room %s (%s)" % (event['room'], event['title']))
			continue

		# generate a task description and put them into the queue
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
				'$id': event['id'],
				'$title': event['title'],
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
		))

	# place a task for the outro into the queue
	queue.put(Rendertask(
		infile = 'outro.svg',
		outfile = 'outro.ts',
		sequence = outroFrames
	))

	# place the pause-sequence into the queue
	queue.put(Rendertask(
		infile = 'pause.svg',
		outfile = 'pause.ts',
		sequence = pauseFrames
	))
