#!/usr/bin/python3

import random
from renderlib import *

scheduleUrl = 'https://events.ccc.de/camp/2015/Fahrplan/schedule.xml'
titlemap = {}

def introFrames(parameters):
	id = parameters['$id']
	title = titlemap[id] if id in titlemap else parameters['$title'].strip()

	rnd = random.Random()
	#rnd.seed(title)
	rnd.seed("blafoo23")

	tiles = range(1, 27)
	targets = {}

	frames = 5*fps
	maxdelay = int(frames/4)

	for tile in tiles:
		targets[tile] = (
			# x/y
			rnd.randint(-1200, -800),
			rnd.randint(-600, 600),

			# delay
			rnd.randint(0, maxdelay)
		)

	# 5 Sekunde Kacheln zusammenbauen
	for i in range(0, frames):
		placements = []
		for tile in tiles:
			delay = targets[tile][2]

			tx = targets[tile][0]
			ty = targets[tile][1]

			x = easeDelay(easeInOutQuad, delay, i, tx, -tx, frames-maxdelay)
			y = easeDelay(easeInOutQuad, delay, i, ty, -ty, frames-maxdelay)

			placements.append(
				('g%u' % tile, 'attr', 'transform', 'translate(%.4f, %.4f)' % (x, y))
			)

		yield placements

def outroFrames(p):
	# 5 Sekunden stehen bleiben
	frames = 5*fps
	for i in range(0, frames):
		yield []

def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		parameters={
			'$id': 6543,
			'$title': 'NSA-Untersuchungsausschuss - Wer kontrolliert wen?',
			'$subtitle': 'A Practical Introduction to Acoustic Cryptanalysis',
			'$person': 'Frantisek Algoldor Apfelbeck'
		}
	)

	# render(
	# 	'outro.svg',
	# 	'../outro.ts',
	# 	outroFrames
	# )

def tasks(queue, args):
	raise NotImplementedError('call with --debug to render your intro/outro')
