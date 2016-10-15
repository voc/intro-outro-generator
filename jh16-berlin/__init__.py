#!/usr/bin/python3


from renderlib import *
from easing import *
from collections import deque

# Please EDIT this URL for each local event of Jugend hackt! ### URL to Schedule-XML
scheduleUrl = 'http://data.c3voc.de/schedule/jh16/schedule-berlin.xml'

# For (really) too long titles
titlemap = {
}

def introFrames(parameters):
	# 8 Sekunden

	# 2 Sekunden Fadein logo und icongroup
	frames = int(2*fps)
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('icongroup',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('alpaca',  'style',    'opacity', 0),
			('text-bg',  'style',    'opacity', 0),
			('projectname',  'style',    'opacity', 0),
			('prenames',  'style',    'opacity', 0),
		)

	# 1 Sekunden Fadein alpaca und text-bg
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', 1),
			('icongroup',  'style',    'opacity', 1),
			('alpaca',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('text-bg',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('projectname',  'style',    'opacity', 0),
			('prenames',  'style',    'opacity', 0),
		)

	# 5 Sekunden Fadein #hack hack hack# projectname + prenames DIREKT einblenden, weil die Schriftart sich nicht faden lässt
	frames = 5*fps
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', 1),
			('icongroup',  'style',    'opacity', 1),
			('alpaca',  'style',    'opacity', 1),
			('text-bg',  'style',    'opacity', 1),
			('projectname',  'style',    'opacity', 1),
			('prenames',  'style',    'opacity', 1),
		)

def outroFrames(parameters):
	# 5 Sekunden

	# 1 Sekunden Fadein logo
	frames = int(1*fps)
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('licensegroup',  'style',    'opacity', 0),
			('logogroup',  'style',    'opacity', 0),
		)

	# 1 Sekunden Fadein licensegroup
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', 1),
			('licensegroup',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('logogroup',  'style',    'opacity', 0),
		)

	# 1 Sekunden Fadein logogroup
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', 1),
			('licensegroup',  'style',    'opacity', 1),
			('logogroup',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	# 2 Sekunden stehen bleiben
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('background',  'style',    'opacity', 1),
			('logo',  'style',    'opacity', 1),
			('licensegroup',  'style',    'opacity', 1),
			('logogroup',  'style',    'opacity', 1),
		)
def backgroundFrames(parameters):
	# 20 Sekunden

	# 10 Sekunden alpaca einblenden
	frames = 10*fps
	for i in range(0, frames):
		yield (
			('background', 'style',	'opacity', 1),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 0.25, 1, frames)),
		)

	# 10 Sekunden alpaca ausblenden
	frames = 10*fps
	for i in range(0, frames):
		yield (
			('background', 'style',	'opacity', 1),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 1, -0.75, frames)),
		)


def pauseFrames(parameters):
	# 6 Sekunden

	# 3 Sekunden alpaca einblenden
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('pause', 'style',	'opacity', "%.4f" % easeInCubic(i, 1, -0.75, frames)),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 0.25, 0.75, frames)),
		)

	# 3 Sekunden alpaca ausblenden
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('pause', 'style',	'opacity', "%.4f" % easeInCubic(i, 0.25, 0.75, frames)),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 1, -0.75, frames)),
		)

def debug():
	s1 = 'Lorem, Ipsum, Ad Dolor... '
	s2 = 'Lorem, Ipsum, Ad Dolor, Sit, Nomen, Est, Omen, Urbi et Orbi... '
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$PROJECTNAME': s1.upper(),
			'$prenames': s2,
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

	render(
		'background.svg',
		'../background.ts',
		backgroundFrames
	)

	render('pause.svg',
		'../pause.ts',
		pauseFrames
	)

def tasks(queue, args):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		#just select room Berlin
		if event['room'] not in ('Berlin'):
			print("skipping room %s (%s)" % (event['room'], event['title']))
			continue

		# generate a task description and put them into the queue
		projectname = event['title']
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
#				'$id': event['id'],
				'$PROJECTNAME': projectname.upper(),
#				'$subtitle': event['subtitle'],
				'$prenames': event['personnames']
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
