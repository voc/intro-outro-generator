#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://vcfb.de/2015/schedule.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}

def introFrames(params):
	move=40

	# 1 Sekunden stillstand
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % 0),
			('subtitle', 'style', 'opacity', "%.4f" % 0),
			('persons', 'style',   'opacity', "%.4f" % 0),
		)

	# 4 Sekunde Text Fadein
	frames = 4*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
			('title', 'attr',     'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),

			('subtitle', 'style', 'opacity', "%.4f" % easeDelay(easeLinear, 1*fps, i, 0, 1, 2*fps)),
			('subtitle', 'attr',  'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 1*fps, i, -move, move, 2*fps)),

			('persons', 'style',   'opacity', "%.4f" % easeDelay(easeLinear, 2*fps, i, 0, 1, 2*fps)),
			('persons', 'attr',    'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 2*fps, i, -move, move, 2*fps)),
		)

	# 2 Sekunden stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield tuple()

def outroFrames(params):
	move=50

	# 1 Sekunden stillstand
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('license', 'style',   'opacity', "%.4f" % 0),
		)

	# 2 Sekunde Text Fadein
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('license', 'style',  'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 2*fps)),
			('license', 'attr',   'transform', 'translate(%.4f, 0)' % easeDelay(easeOutQuad, 0*fps, i, -move, move, 2*fps)),
		)

	# 2 Sekunden stillstand
	frames = 2*fps
	for i in range(0, frames):
		yield tuple()


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
