#!/usr/bin/python3

import svg.path
from lxml import etree
from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://programm.froscon.de/2015/schedule.xml'

def introFrames(args):
	xml = etree.parse('froscon2015/artwork/intro.svg').getroot()
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
		yield tuple()

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('bar',   'style', 'opacity', easeLinear(i, 1, -1, frames)),
			('title', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield (
			('bar',   'style', 'opacity', 0),
			('title', 'style', 'opacity', 0),
		)

def outroFrames(args):
	xml = etree.parse('froscon2015/artwork/outro.svg').getroot()
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
		yield tuple()

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('license',   'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
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
		'../intro.dv',
		introFrames,
		{
			'$id': 1302,
			'$title': 'VlizedLab - Eine Open Source-Virtualisierungslösung für PC-Räume',
			'$subtitle': 'IT Automatisierung und zentrales Management mit SALT',
			'$personnames': 'Thorsten Kramm'
		}
	)

	render('outro.svg',
		'../outro.dv',
		outroFrames
	)

	render('pause.svg',
		'../pause.dv',
		pauseFrames
	)


def tasks(queue, args):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['room'] not in ('HS 1', 'HS 2', 'HS 1/2', 'HS 3', 'HS 4', 'HS 5', 'HS 6', 'HS 7', 'HS 8'):
			print("skipping room %s (%s)" % (event['room'], event['title']))
			continue

		# generate a task description and put them into the queue
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".dv",
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
		outfile = 'outro.dv',
		sequence = outroFrames
	))

	# place the pause-sequence into the queue
	queue.put(Rendertask(
		infile = 'pause.svg',
		outfile = 'pause.dv',
		sequence = pauseFrames
	))
