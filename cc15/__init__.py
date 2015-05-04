#!/usr/bin/python3

import subprocess
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'http://www.fossgis.de/konferenz/2014/programm/schedule.de.xml'

# For (really) too long titles
titlemap = {
}


def outroFrames(parameters):
	# 5 Sekunden

	# 1 Sekunden Pause
	frames = 1*fps
	for i in range(0, frames):
		yield (
		)

	# 3 Sekunde Fade-out to sublab
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('cc15logo',   'style', 'opacity', "%.4f" % easeOutCubic(i, 1, -1, frames)),
			('backdrop',   'style', 'opacity', "%.4f" % easeOutCubic(i, 1, -1, frames)),
			('sublab',     'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
		)

	# 1 Sekunde Pause
	frames = 1*fps
	for i in range(0, frames):
		yield (
		)

def introFrames(parameters):
	# 5 Sekunden

	# 2 Sekunden Fade-in
	frames = 2*fps
	for i in range(0, frames):
		yield (
                        ('box',           'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 0.6627451, frames)),
			('personname',   'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
			('title',         'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
		)

	# 3 Sekunden stehen bleiben
	frames = 3*fps
	for i in range(0, frames):
		yield (
		#	('box',           'style', 'opacity', '0.6627451'),
		#	('personname',   'style', 'opacity', '1'),
		#	('title',         'style', 'opacity', '1'),
		)

def pauseFrames(parameters):
	# 12 Sekunden

	# 2 Sekunden Text1 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text-de', 'style', 'opacity', 1),
			('text-en', 'style', 'opacity', 0)
		)

	# 2 Sekunden Fadeout text-de
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text-de', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
			('text-en', 'style', 'opacity', 0)
		)

	# 2 Sekunden Fadein text-en
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text-de', 'style', 'opacity', 0),
			('text-en', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames))
		)

	# 2 Sekunden text-en stehen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text-de', 'style', 'opacity', 0),
			('text-en', 'style', 'opacity', 1)
		)

	# 2 Sekunden Fadeout text-en
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text-de', 'style', 'opacity', 0),
			('text-en', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames)))
		)

	# 2 Sekunden Fadein text-de
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text-de', 'style', 'opacity', "%.4f" % (easeOutCubic(i, 0, 1, frames))),
			('text-en', 'style', 'opacity', 0)
		)

def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': 667,
			'$title': 'Wir kochen Hagebuttenmarmelade und denken uns lange Vortragsnamen aus',
			'$subtitle': '',
			'$personnames': 'Prof. Wolfgang Kleinwächter'
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

def ticket(ticket):
	return Rendertask(
		infile = 'intro.svg',
		sequence = introFrames,
		parameters = {
			'$id': ticket['Fahrplan.ID'],
			'$title': ticket.get('Fahrplan.Title'),
			'$subtitle': ticket.get('Fahrplan.Subtitle'),
			'$personnames': ticket.get('Fahrplan.Person_list')
		}
	)

def deploy(ticket, task):
	for encoder in range(1, 6):
		print(colored("--> rsync'ing to encoder{n}".format(n=encoder), 'green'))
		subprocess.check_call('rsync -v --bwlimit=1000 --progress -e="ssh -A voc@gw.ep14.c3voc.de ssh -A voc@encoder{n}.lan.c3voc.de" {file} :{file}'.format(n=encoder, file=task.outfile), shell=True)
