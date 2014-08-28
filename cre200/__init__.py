#!/usr/bin/python3

from renderlib import *

def outroFrames():
	# 8 Sekunden

	# 1 Sekunden stehen bleiben
	frames = int(1*fps)
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('lizenz','style',    'opacity', 1),
		)

	# 4 Sekunde Fadeout Logo
	frames = 4*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 1, -1, frames)),
			('lizenz','style',    'opacity', 1),
		)

	# 4 Sekunde Fadeout Logo
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 0),
			('lizenz','style',    'opacity', "%.4f" % easeInCubic(i, 1, -1, frames)),
		)

	# 3 Sekunden stehen bleiben
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 0),
			('lizenz','style',    'opacity', 0),
		)

def introFrames():
	# 8 Sekunden

	# 2 Sekunden Fadein logo
	frames = int(2*fps)
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('text',  'style',    'opacity', 0),
		)

	# 3 Sekunden Fadein text
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('text',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	# 3 Sekunden stehen bleiben
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('text',  'style',    'opacity', 1),
		)

def pauseFrames():
	# 8 Sekunden im kresi drehen
	frames = int(8*fps)
	for i in range(0, frames):
		yield (
			('logo',  'attr',     'transform', 'translate(%.4f, %.4f)' % (math.sin(i / frames * math.pi * 2) * 200, math.cos(i / frames * math.pi * 2) * 180) ),
		)


def debug():
	render(
		'pause.svg',
		'../pause.dv',
		pauseFrames
	)

	render(
		'intro.svg',
		'../intro.dv',
		introFrames
	)

	render(
		'outro.svg',
		'../outro.dv',
		outroFrames
	)

def tasks(queue):
	# generate a task description and put them into the queue
	queue.put(Rendertask(
		infile = 'intro.svg',
		outfile = "intro.dv",
		sequence = introFrames
	))

	# place a task for the outro into the queue
	queue.put(Rendertask(
		infile = 'outro.svg',
		outfile = 'outro.dv',
		sequence = outroFrames
	))
