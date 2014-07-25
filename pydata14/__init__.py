#!/usr/bin/python

import subprocess
import os.path
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'file://' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schedule.xml')

# For (really) too long titles
titlemap = {
	
}

def introFrames():
	frames = int(.5*fps)
	for i in range(0, frames):
		yield (
			('name', 'style', 'fill-opacity', 0),
			('title', 'style', 'fill-opacity', 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('name', 'style', 'fill-opacity', '%.4f' % easeInCubic(i, 0, 1, 3*fps)),
			('title', 'style', 'fill-opacity', 0),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('name', 'style', 'fill-opacity', '%.4f' % easeInCubic(i+1*fps, 0, 1, 3*fps)),
			('title', 'style', 'fill-opacity', '%.4f' % easeInCubic(i, 0, 1, 3*fps)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('name', 'style', 'fill-opacity', 1),
			('title', 'style', 'fill-opacity', '%.4f' % easeInCubic(i+2*fps, 0, 1, 3*fps)),
		)

	frames = 3*fps
	for i in range(0, frames):
		yield (
			('name', 'style', 'fill-opacity', 1),
			('title', 'style', 'fill-opacity', 1),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('name', 'style', 'fill-opacity', easeLinear(i, 1, -1, frames)),
			('title', 'style', 'fill-opacity', easeLinear(i, 1, -1, frames)),
		)

def outroFrames():
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % easeInCubic(i, 0, 1, 3*fps)),
			('text', 'style', 'opacity', 0),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % easeInCubic(i+1*fps, 0, 1, 3*fps)),
			('text', 'style', 'opacity', '%.4f' % easeInCubic(i, 0, 1, 3*fps)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', 1),
			('text', 'style', 'opacity', '%.4f' % easeInCubic(i+2*fps, 0, 1, 3*fps)),
		)

	frames = 3*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', 1),
			('text', 'style', 'opacity', 1),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
			('text', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
		)

def debug():
	render(
		'outro.svg',
		'../outro.dv',
		outroFrames
	)

	render(
		'intro.svg',
		'../intro.dv',
		introFrames,
		{
			'$id': 20227,
			'$title': "Driving Moore's Law with Python-Powered Machine Learning: An Insider's Perspective",
			'$subtitle': '',
			'$personnames': 'Felix Marczinowski, Philipp Mack, Sönke Niekamp'
		}
	)

def tasks(queue):
	uid = []
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['id'] in uid:
			continue

		uid.append(event['id'])

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
