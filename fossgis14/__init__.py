#!/usr/bin/python3

import subprocess
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'http://www.fossgis.de/konferenz/2014/programm/schedule.de.xml'

# For (really) too long titles
titlemap = {
	708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}


def outroFrames():
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

def introFrames():
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

def pauseFrames():
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
		'../intro.dv',
		introFrames,
		{
			'$id': 667,
			'$title': 'OpenJUMP - Überblick, Neuigkeiten, Zusammenarbeit/Schnittstellen mit proprietärer Software',
			'$subtitle': 'Even more news about OpenJUMP',
			'$personnames': 'Matthias Scholz'
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

	# place the pause-sequence into the queue
	queue.put(Rendertask(
		infile = 'pause.svg',
		outfile = 'pause.dv',
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
