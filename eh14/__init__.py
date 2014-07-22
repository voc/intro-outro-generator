#!/usr/bin/python3

from renderlib import *
import math

# URL to Schedule-XML
scheduleUrl = 'http://eh14.easterhegg.eu/pages/fahrplan/schedule.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}


def outroFrames():
	# 5 Sekunden

	# 2 Sekunden Fadein Lizenz
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('lizenz','style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	# 3 Sekunden stehenlassen
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('lizenz','style',    'opacity', 1),
		)

def introFrames():
	# 5 Sekunden

	# 1 Sekunde Title Fadein
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('text',  'style',    'opacity', 0),
			('lizenz','style',    'opacity', 0),
		)

	# 2 Sekunde Text Fadein
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', 1),
			('text',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('lizenz','style',    'opacity', 0),
		)

	# 1 Sekunde Lizenz Fadein
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', 1),
			('text',  'style',    'opacity', 1),
			('lizenz','style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	# 1 Sekunde stehen bleiben
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('title', 'style',    'opacity', 1),
			('text',  'style',    'opacity', 1),
			('lizenz','style',    'opacity', 1),
		)

def pauseFrames():
	# 7 Sekunden

	# 3 Sekunde Text FadeIn
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('text','style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	# 3 Sekunde Text FadeOut
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('text','style',    'opacity', "%.4f" % easeInCubic(i, 1, -1, frames)),
		)

	# 1 Sekunde stehen lassen
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text','style',    'opacity', 0),
		)

def debug():
	render(
		'intro.svg',
		'../intro.dv',
		introFrames,
		{
			'$id': 5725,
			'$title': 'Sleep? Ain\'t nobody got time for that!',
			'$subtitle': 'Physiologie von Schlaf und Wachzustand',
			'$personnames': 'Christina'
		}
	)

	render(
		'outro.svg',
		'../outro.dv',
		outroFrames
	)

	render('pause.svg',
		'../pause.dv',
		pauseFrames
	)

def tasks(queue):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):

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
