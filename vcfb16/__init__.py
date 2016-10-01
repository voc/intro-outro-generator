#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://geruempel.ddns.net/schedule_voc.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}

def introFrames(params):
	move=40

	# 0.5 Seconds
	frames = int(0.5*fps)
	for i in range(0, frames):
		yield (
			('title',       'style', 'opacity', "%.4f" % 0),
			('subtitle',    'style', 'opacity', "%.4f" % 0),
			('personnames', 'style', 'opacity', "%.4f" % 0),
		)

	# 3 Sekunde Text Fadein
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
			('title', 'attr',     'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),

			('subtitle', 'style', 'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
			('subtitle', 'attr',  'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),

			('personnames', 'style', 'opacity', "%.4f" % easeDelay(easeLinear, 1*fps, i, 0, 1, 2*fps)),
			('personnames', 'attr',  'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 1*fps, i, -move, move, 2*fps)),
		)

	# 2 Sekunden stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield tuple()

	# 1 Sekunde fadeout
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style', 'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
			('subtitle', 'style', 'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
			('personnames', 'style', 'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
		)

	# 0.5 Sekunden stillstand
	frames = int(0.5*fps)
	for i in range(0, frames):
		yield (
			('title', 'style', 'opacity', "%.4f" % 0),
			('subtitle', 'style', 'opacity', "%.4f" % 0),
			('personnames', 'style', 'opacity', "%.4f" % 0),
		)

def outroFrames(params):
	move=50

	# 1 Sekunden stillstand
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('license', 'style',   'opacity', "%.4f" % 0),
		)

	# 4 Sekunde Text Fadein
	frames = 4*fps
	for i in range(0, frames):
		yield (
			('license', 'style',  'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
			('license', 'attr',   'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),
		)

	# 2 Sekunden stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('license', 'style',   'opacity', "%.4f" % 1),
		)


def pauseFrames(params):
	# 1 Sekunden fade down
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('break', 'style',   'opacity', "%.4f" % easeLinear(i, 0.5, +0.5, frames)),
		)

	# 1 Sekunden fade up
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('break', 'style',   'opacity', "%.4f" % easeLinear(i, 1, -0.5, frames)),
		)

def debug():
#	 render(
#	 	'outro.svg',
#	 	'../outro.ts',
#	 	outroFrames
#       )

#	 render(
#		'pause.svg',
#		'../pause.ts',
#		pauseFrames
#	)

	 render(
	 	'intro.svg',
	 	'../intro.ts',
	 	introFrames,
	 	{
	 		'$id': 904,
	 		'$title': 'Was ist Open Source, wie funktioniert das?',
	 		'$subtitle': 'Die Organisation der Open Geo- und GIS-Welt. Worauf man achten sollte.',
	 		'$personnames': 'Arnulf Christl, Astrid Emde, Dominik Helle, Till Adams'
	 	}
	 )

def tasks(queue, params):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl, titlemap):

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
