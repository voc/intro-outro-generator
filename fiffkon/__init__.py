#!/usr/bin/python3

from renderlib import *
import math

# URL to Schedule-XML
scheduleUrl = 'http://2014.fiff.de/app/schedule.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}


def outroFrames(p):
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('logo',   'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('plate',  'style',    'opacity', 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('logo',   'style',    'opacity', 1),
			('plate',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('logo',   'style',    'opacity', 1),
			('plate',  'style',    'opacity', 1),
		)

def introFrames(p):
	frames = math.floor(1.5*fps)
	for i in range(0, frames):
		yield (
			('header', 'attr',    'y',       659),
			('text',  'style',    'opacity', 0),
		)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('header', 'attr',    'y',       "%.4f" % easeInOutQuad(i, 659, 499-659, frames)),
			('text',  'style',    'opacity', 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	frames = math.ceil(2.5*fps)
	for i in range(0, frames):
		yield (
			('text',  'style',    'opacity', 1),
		)

def pauseFrames(p):
	pass


def debug():
	render(
		'intro.svg',
		'../intro.dv',
		introFrames,
		{
			'$id': 6526,
			'$title': 'Nachrichtendienstliche Zugriffe auf Telekommunikation und IKT-Strukuren und ihre Implikationen für individuelle und staatliche Souveränität',
			'$subtitle': '',
			'$personnames': 'Andy Müller-Maguhn'
		}
	)

	render(
		'outro.svg',
		'../outro.dv',
		outroFrames
	)

	# render('pause.svg',
	# 	'../pause.dv',
	# 	pauseFrames
	# )

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

	# # place the pause-sequence into the queue
	# queue.put(Rendertask(
	# 	infile = 'pause.svg',
	# 	outfile = 'pause.dv',
	# 	sequence = pauseFrames
	# ))
