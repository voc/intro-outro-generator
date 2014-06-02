#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math

# URL to Schedule-XML
scheduleUrl = 'http://sotm-eu.org/export.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}


def outroFrames():
	# 9 Sekunden

	# 3 Sekunden Fadein Logo
	frames = int(3*fps)
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('box',   'style',    'opacity', 0)
		)

	# 3 Sekunde Fadein Box
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('box',   'style',    'opacity', "%.4f" % easeOutQuad(i, 0, 1, frames)),
			('box',   'attr',     'transform', 'translate(0,%.4f)' % easeOutQuad(i, 94, -94, frames) )
			#('box',   'attr',     'transform', 'translate(%.4f,0)' % easeOutQuad(i, 960, -960, frames) )
		)

	# 3 Sekunden stehen bleiben
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('box',   'style',    'opacity', 1)
		)


def introFrames():
	# 7 Sekunden

	# 0.5 Sekunden stehen bleiben
	frames = int(math.ceil(0.5*fps))
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 0),
			('box',   'style',    'opacity', 0)
		)

	# 1.5 Sekunden Fadein Logo
	frames = int(math.ceil(1.5*fps))
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('box',   'style',    'opacity', 0)
		)

	# 3 Sekunde Fadein Box
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('box',   'style',    'opacity', "%.4f" % easeOutQuad(i, 0, 1, frames)),
			('box',   'attr',     'transform', 'translate(0,%.4f)' % easeOutQuad(i, 198, -198, frames) )
			#('box',   'attr',     'transform', 'translate(%.4f,0)' % easeOutQuad(i, 960, -960, frames) )
		)

	# 3 Sekunden stehen bleiben
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', 1),
			('box',   'style',    'opacity', 1)
		)

def pauseFrames():
	# 12 Sekunden

	texts = {
		'text1': "0.0",
		'text2': "0.0",
		'text3': "0.0"
	}

	for name in texts.keys():
		# 2 Sekunden einfaden
		frames = 2*fps
		for i in range(0, frames):
			texts[name] = "%.4f" % easeOutQuad(i, 0, 1, frames)

			yield (
				('text1', 'style',	'opacity', texts['text1']),
				('text2', 'style',	'opacity', texts['text2']),
				('text3', 'style',	'opacity', texts['text3'])
			)

		# 2 Sekunden ausfaden
		frames = 2*fps
		for i in range(0, frames):
			texts[name] = "%.4f" % easeOutQuad(i, 1, -1, frames)

			yield (
				('text1', 'style',	'opacity', texts['text1']),
				('text2', 'style',	'opacity', texts['text2']),
				('text3', 'style',	'opacity', texts['text3'])
			)

		texts[name] = "0.0"

def debug():
	render(
		'intro.svg',
		'../intro.dv',
		introFrames,
		{
			'$id': 667,
			'$title': 'OpenJUMP - Überblick, Neuigkeiten, Zusammenarbeit/Schnittstellen mit proprietärer Software',
			'$subtitle': 'Even more news about OpenJUMP',
			'$personnames': 'Matthias S.'
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
	for event in events():

		# generate a task description and put them into the queue
		queue.put((
			'intro.svg',
			str(event['id'])+".dv",
			introFrames,
			{
				'$id': event['id'],
				'$title': event['title'],
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
		))

	# place a task for the outro into the queue
	queue.put((
		'outro.svg',
		'outro.dv',
		outroFrames
	))

	# place the pause-sequence into the queue
	queue.put((
		'pause.svg',
		'pause.dv',
		pauseFrames
	))
