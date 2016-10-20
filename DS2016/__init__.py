#!/usr/bin/python3

from lxml import etree
from slugify import slugify
from renderlib import *
from renderlib import *
from easing import *


# URL to Schedule-XML
scheduleUrl = 'https://www.datenspuren.de/2016/fahrplan/schedule.xml'

# For (really) too long titles
titlemap = {

}

def introFrames(parameters):
	frames = round(0.5*fps)
	for i in range(0, frames):
		yield (
			('names', 'style', 'opacity', 0),
			('title', 'style', 'opacity', 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('names', 'style', 'opacity', 0),
			('title', 'style', 'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('names', 'style', 'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('title', 'style', 'opacity', 1),
		)

	frames = 4*fps
	for i in range(0, frames):
		yield (
			('names', 'style', 'opacity', 1),
			('title', 'style', 'opacity', 1),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('names', 'style', 'opacity', "%.4f" % easeOutCubic(i, 1, -1, frames)),
			('title', 'style', 'opacity', "%.4f" % easeOutCubic(i, 1, -1, frames)),
		)

	#frames = 1*fps
	#for i in range(0, frames):
	#	yield (
	#		('names', 'style', 'opacity', 0),
	#		('title', 'style', 'opacity', 0),
	#	)

def debug():
	render('intro.svg',
		'../intro.dv',
		introFrames,
		{
			'$id': 5924,
			'$title': 'Digitale Selbstverteidigung - Wie schütze ich mich vor Überwachung?',
			'$subtitle': '',
			'$personnames': 'Chaostreff Chemnitz, Eva Olivin, Robert Verch'
		}
	)

	# render('outro.svg',
	# 	'../outro.dv',
	# 	outroFrames
	# )

def tasks(queue, args):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
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
