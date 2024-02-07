#!/usr/bin/python3

import random, sys
from renderlib import *
from schedulelib import *
from easing import *
from colour import Color

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
	# 3 Sekunden Logo
	frames = 10
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % 0),
			('logo', 'style', 'opacity', '%.4f' % 0),
		)

	# 3 Sekunden Logo
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % 0),
			('logo', 'style', 'opacity', '%.4f' % easeLinear(i, 0, 1, frames)),
		)

	# 1 Sekunde Stillstand
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % 0),
			('logo', 'style', 'opacity', '%.4f' % 1),
		)

	# 2 Sekunden Lizenz
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % easeLinear(i, 0, 1, frames)),
			('logo', 'style', 'opacity', '%.4f' % 1),
		)

	# 2 Sekunden Stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % 1),
			('logo', 'style', 'opacity', '%.4f' % 1),
		)

	# 2 Sekunden Fadeout
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('plate', 'style', 'opacity', '%.4f' % easeLinear(i, 1, -1, frames)),
			('logo', 'style', 'opacity', '%.4f' % easeLinear(i, 1, -1, frames)),
		)

def supersourceFrames(p):
	counts = {
		'brown': 4,
		'green': 7,
		'orange': 5,
		'purple': 4,
		'blueish': 4,
	}

	sequences = {
		'brown': ['brown', 'orange', 'purple', 'blueish', 'brown'],
		'green': ['green', 'purple', 'blueish', 'orange', 'green'],
		'orange': ['orange', 'blueish', 'brown', 'green', 'orange'],
		'purple': ['purple', 'orange', 'green', 'blueish', 'purple'],
		'blueish': ['blueish', 'brown', 'green', 'purple', 'blueish'],
	}

	bgs = {
		'brown': Color('#94694d'),
		'green': Color('#6c9e30'),
		'orange': Color('#e1983a'),
		'purple': Color('#77438d'),
		'blueish': Color('#707f9a'),
	}

	grids = {
		'brown': Color('#7a563f'),
		'green': Color('#598227'),
		'orange': Color('#ba7d2f'),
		'purple': Color('#623672'),
		'blueish': Color('#5c687e'),
	}

	bg_frames = {}
	grid_frames = {}

	frames_per_transition = 5*fps
	num_transitions = 0

	for name in sequences:
		bg_frames[name] = []
		grid_frames[name] = []
		sequence = sequences[name]
		num_transitions = len(sequence)

		for transition in range(1, len(sequence)):
			start = sequence[transition-1]
			end = sequence[transition]

			bg_frames[name].extend(
				bgs[start].range_to(bgs[end], frames_per_transition)
			)
			grid_frames[name].extend(
				grids[start].range_to(grids[end], frames_per_transition)
			)

	frames = frames_per_transition * (num_transitions - 1)

	for frame in range(0, frames):
		changes = []
		for name in sequences:
			for idx in range(0, counts[name]+1):
				changes.extend([
					('bg-%s-%u' % (name, idx), 'style', 'fill', bg_frames[name][frame]),
					('grid-%s-%u' % (name, idx), 'style', 'fill', grid_frames[name][frame]),
				])

		yield changes

def debug():
	render(
		'intro.svg',
		'../6983.ts',
		introFrames,
		parameters={
			'$id': 6983,
			'$title': 'Infrastructure Review',
			'$subtitle': '',
			'$personnames': 'Will, Arjen, MaZderMind, Fengel'
		}
	)

	# render(
	# 	'intro.svg',
	# 	'../8.ts',
	# 	introFrames,
	# 	parameters={
	# 		'$id': 8,
	# 		'$title': 'The Incredible Herrengedeck',
	# 		'$subtitle': 'Chanson-Punk aus Berlin',
	# 		'$personnames': ''
	# 	}
	# )

	# render(
	# 	'outro.svg',
	# 	'../outro.ts',
	# 	outroFrames
	# )

	# render(
	# 	'supersource.svg',
	# 	'../supersource.ts',
	# 	supersourceFrames
	# )

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

	queue.put(Rendertask(
		infile = 'supersource.svg',
		outfile = 'supersource.ts',
		sequence = supersourceFrames
	))
