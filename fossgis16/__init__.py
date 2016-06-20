#!/usr/bin/python3

import subprocess
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://frab.fossgis-konferenz.de/de/2016/public/schedule.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}


def outroFrames(params):
	# 5 Sekunden

	# 2 Sekunden Fadein Text
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('banderole', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames) ),
			('license', 'style', 'opacity', 0)
		)

	# 2 Sekunde Fadein Lizenz-Logo
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('banderole', 'style', 'opacity', 1),
			('license', 'style', 'opacity', "%.4f" % (float(i)/frames))
		)

	# 1 Sekunde stehen bleiben
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('banderole', 'style', 'opacity', 1),
			('license', 'style', 'opacity', 1)
		)

def introFrames(params):
	# 7 Sekunden

	# 2 Sekunden Text 1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box',   'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
			('url',   'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
			('text1', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
			('text2', 'style', 'opacity', 0)
		)

	# 1 Sekunde Fadeout Text 1
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('box',   'style', 'opacity', 1),
			('url',   'style', 'opacity', 1),
			('text1', 'style', 'opacity', "%.4f" % (1-(float(i)/frames))),
			('text2', 'style', 'opacity', 0)
		)

	# 2 Sekunden Text 2
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box',   'style', 'opacity', 1),
			('url',   'style', 'opacity', 1),
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames))
		)

	# 2 Sekunden stehen bleiben
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box',   'style', 'opacity', 1),
			('url',   'style', 'opacity', 1),
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', 1)
		)

def pauseFrames(params):
	# 12 Sekunden

	# 2 Sekunden Text1 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 1),
			('text2', 'style', 'opacity', 0)
		)

	# 2 Sekunden Fadeout Text1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
			('text2', 'style', 'opacity', 0)
		)

	# 2 Sekunden Fadein Text2
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames))
		)

	# 2 Sekunden Text2 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', 1)
		)

	# 2 Sekunden Fadeout Text2
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames)))
		)

	# 2 Sekunden Fadein Text1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', "%.4f" % (easeOutCubic(i, 0, 1, frames))),
			('text2', 'style', 'opacity', 0)
		)

def debug():
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

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

	render('pause.svg',
		'../pause.ts',
		pauseFrames
	)

def tasks(queue):
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
