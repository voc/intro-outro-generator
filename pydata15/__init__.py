#!/usr/bin/python

import subprocess
import os.path
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'https://raw.githubusercontent.com/pydataberlin/pydataberlin.github.io/master/utils/pydata_berlin_voc.xml'

# For (really) too long titles
titlemap = {
	69233462: 'pyData Berlin 2015: keynote'
}

def introFrames(parameters):
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

def outroFrames(parameters):
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


def pauseFrames(parameters):
	frames = 10*fps
	for i in range(0, frames):
		yield (
			('pause1', 'attr',   'x', '%.4f' % easeLinear(i, -268, 1295, frames)),
			('pause1', 'style', 'opacity', 1),
			('pause2', 'style', 'opacity', 0),
		)

	frames = 10*fps
	for i in range(0, frames):
		yield (
			('pause2', 'attr',   'x', '%.4f' % easeLinear(i, -268, 1295, frames)),
			('pause2', 'style', 'opacity', 1),
			('pause1', 'style', 'opacity', 0),
		)

def debug():
	render(
		'pause.svg',
		'../pause.dv',
		pauseFrames
	)

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

def tasks(queue, parameters):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):

		# generate a task description and put it into the queue
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

	# generate a task description and put it into the queue
	queue.put(Rendertask(
		infile = 'outro.svg',
		outfile = 'outro.dv',
		sequence = outroFrames
	))

	# generate a task description and put it into the queue
	queue.put(Rendertask(
		infile = 'pause.svg',
		outfile = 'pause.dv',
		sequence = pauseFrames
	))
