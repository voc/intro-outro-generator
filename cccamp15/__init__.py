#!/usr/bin/python3

import random, sys
from renderlib import *
from easing import *

scheduleUrl = 'https://events.ccc.de/camp/2015/Fahrplan/schedule.xml'
titlemap = {}

def introFrames(parameters):
	id = parameters['$id']
	title = titlemap[id] if id in titlemap else parameters['$title'].strip()

	rnd = random.Random()
	rnd.seed(id)

	tiles = range(1, 28)
	targets = {}

	frames = 5*fps
	useddelay = 0
	maxdelay = int(frames/2)

	for tile in tiles:
		delay = rnd.randint(0, maxdelay)
		useddelay = max(useddelay, delay)
		targets[tile] = (
			# x/y
			rnd.randint(-1200, -900),
			rnd.randint(-600, 600),

			# delay
			delay
		)

	print('useddelay=%u maxdelay=%u' % (useddelay, maxdelay))

	# 5 Sekunde Kacheln zusammenbauen
	for i in range(0, frames+useddelay):
		placements = []
		for tile in tiles:
			delay = targets[tile][2]

			tx = targets[tile][0]
			ty = targets[tile][1]

			x = easeDelay(easeOutQuint, delay, i, tx, -tx, frames)
			y = easeDelay(easeOutQuint, delay, i, ty, -ty, frames)

			placements.append(
				('g%u' % tile, 'attr', 'transform', 'translate(%.4f, %.4f)' % (x, y))
			)

		x = easeDelay(easeOutQuint, frames, i, -25, 25, useddelay)
		opacity = easeDelay(easeLinear, frames, i, 0, 1, useddelay)

		placements.extend([
			('text', 'style', 'opacity', '%.4f' % opacity),
			('text', 'attr', 'transform', 'translate(%.4f, 0)' % x),
			('rocket', 'style', 'opacity', '0'),
		])

		yield placements


	# final placement
	placements = []
	for tile in tiles:
		placements.append(
			('g%u' % tile, 'attr', 'transform', 'translate(%.4f, %.4f)' % (0, 0)),
		)

	placements.extend([
		('text', 'style', 'opacity', '%.4f' % 1),
		('text', 'attr', 'transform', 'translate(%.4f, 0)' % 0)
	])

	# final frame
	yield placements

	# start rotation
	dr = 30

	# start point
	dx = -890
	dy = 660

	# distance from origin
	ox = 830
	oy = 576

	# landing height
	lh = 15

	# fly the rocket
	frames = 3*fps
	for i in range(0, frames):
		r = easeOutQuad(i, dr, -dr, frames)
		x = easeOutQuad(i, dx, -dx, frames)
		y = easeOutQuad(i, dy, -dy - lh, frames)

		yield (
			('rocket', 'style', 'opacity', '1'),
			('rocket', 'attr', 'transform', 'translate(%.4f, %.4f) rotate(%.4f, %.4f, %.4f)' % (x, y, r, ox, oy)),
		)

	# land the rocket
	frames = 1*fps
	for i in range(0, frames):
		y = easeLinear(i, -lh, lh, frames)

		yield (
			('rocket', 'attr', 'transform', 'translate(0, %.4f)' % y),
		)

	print('remaining frames=%u' % (maxdelay - useddelay))
	# stay there 1.5s + fill up flyin-delay
	frames = 25+13 + maxdelay - useddelay
	for i in range(0, frames):
		yield (
			('rocket', 'attr', 'transform', 'translate(0, 0)'),
		)

	# fade all out 0.5 s
	frames = 12
	for i in range(0, frames):
		yield (
			('fade', 'attr', 'x', '0'),
			('fade', 'attr', 'y', '0'),
			('fade', 'style', 'opacity', '%.4f' % easeLinear(i, 0, 1, frames)),
		)

	# final frame
	yield (
		('fade', 'style', 'opacity', '1'),
	)

def outroFrames(p):
	# 3 Sekunden Stillstand
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % 0),
		)

	# 2 Sekunden Lizenz
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % easeLinear(i, 0, 1, frames)),
		)

	# 2 Sekunden Stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % 1),
		)

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

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

def tasks(queue, args):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):

		# HACK: only render event 49
		#if event['id'] != 49:
		#	continue

		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
				'$id': event['id'],
				'$title': event['title'].upper(),
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
		))

	queue.put(Rendertask(
		infile = 'outro.svg',
		outfile = 'outro.ts',
		sequence = outroFrames
	))
