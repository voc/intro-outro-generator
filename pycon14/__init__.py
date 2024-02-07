#!/usr/bin/python

import subprocess
from renderlib import *
from schedulelib import *

# URL to Schedule-XML
scheduleUrl = 'https://ep2014.europython.eu/schedule.frab.xml'

# For (really) too long titles
titlemap = {

}

def pyconFrames():
	givenFrame = 0

	frames = 168
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('text', 'style', 'opacity', 0),
		)

	frames = 16
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',   'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('text', 'style', 'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
		)

	frames = 113
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('text', 'style', 'opacity', 1),
		)

	frames = 14
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('text', 'style', 'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
		)

	frames = 65
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('text', 'style', 'opacity', 0),
		)

def debug():
	render(
		'intro.svg',
		'../intro.dv',
		pyconFrames,
		{
			'$id': 93,
			'$title': 'Deploying and managing FreeBSD jails with mr.awsome, fabric and ansible',
			'$subtitle': '',
			'$personnames': 'tomster'
		}
	)

def tasks(queue):
	uid = []
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['id'] in uid:
			continue

		uid.append(event['id'])

		# generate a task description and put them into the queue
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".dv",
			sequence = pyconFrames,
			parameters = {
				'$id': event['id'],
				'$title': event['title'],
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
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
	for encoder in range(1, 3):
		print(colored("--> rsync'ing to encoder{n}".format(n=encoder), 'green'))
		subprocess.check_call('rsync -v --bwlimit=1000 --progress -e="ssh -A voc@gw.ep14.c3voc.de ssh -A voc@encoder{n}.lan.c3voc.de" {file} :/tmp/'.format(n=encoder, file=task.outfile), shell=True)
