#!/usr/bin/python3

import svg.path, random
from lxml import etree
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'http://fahrplan.mrmcd.net/schedule.xml'

# For (really) too long titles
titlemap = {
	6037: 'End-to-Display Verschlüsselung',
	5985: 'Dem Stromnetz auf die Finger geguckt',
	6036: 'Nuclear Dis-armament Hacks',
	6032: 'Baustellen-eröffnung',
	6029: 'Arduino Tempera-turmessungen',
	6028: 'Geheimdienste und Spione',
	6026: 'Die Kunst, von der Kunst zu leben',
	6000: 'ChaosFamilien Duell',
	5977: 'Security Nightmar es for Journalists',
	5957: 'Verhandlungen & Kommunikation',
	5906: 'Quanten-kryptographie',
	5821: 'angewandte konsensdemokratie',
}

def introFrames(parameters):
	id = parameters['$id']
	title = titlemap[id] if id in titlemap else parameters['$title'].strip()

	rnd = random.Random()
	rnd.seed(title)
	frames = 0

	yield (
		('namesbar', 'style', 'opacity', 0),
		('title', 'text', None, ''),
		('titleHidden', 'text', None, ''),
	)

	for char in range(0, len(title) + 1):
		for holdframe in range(0, rnd.randint(2, 10)):
			frames += 1
			yield (
				('title', 'text', None, title[:char]),
				('titleHidden', 'text', None, title[char:]),
			)

	frames = 4*fps
	for i in range(0, frames):
		yield (
			('namesbar', 'style', 'opacity', 1),
		)

def outroFrames(parameters):

	frames = int(0.5*fps)
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 0),
			('bar1', 'style', 'opacity', 0),
			('bar2', 'style', 'opacity', 0),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 0),
			('bar2', 'style', 'opacity', 0),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(0.5*fps)
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 1),
			('bar2', 'style', 'opacity', 0),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 1),
			('bar2', 'style', 'opacity', 1),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(3.5*fps)
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 1),
			('bar2', 'style', 'opacity', 1),
			('bar3', 'style', 'opacity', 1),
		)

def debug():
	render('intro.svg',
		'../intro.dv',
		introFrames,
		{
			'$id': 5924,
			'$title': 'Eliminating DOM-based XSS',
			'$subtitle': '',
			'$personnames': 'Tobias Mueller'
		}
	)

	# render('outro.svg',
	# 	'../outro.dv',
	# 	outroFrames
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
