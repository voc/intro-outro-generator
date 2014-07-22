#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

	# render(
	# 	'outro.svg',
	# 	'../outro.dv',
	# 	outroFrames
	# )

	# render('pause.svg',
	# 	'../pause.dv',
	# 	pauseFrames
	# )

def tasks(queue):
	uid = []
	# iterate over all events extracted from the schedule xml-export
	for event in events():
		if event['id'] in uid:
			continue

		uid.append(event['id'])

		# generate a task description and put them into the queue
		queue.put((
			'intro.svg',
			str(event['id'])+".dv",
			pyconFrames,
			{
				'$id': event['id'],
				'$title': event['title'],
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
		))

	# # place a task for the outro into the queue
	# queue.put((
	# 	'outro.svg',
	# 	'outro.dv',
	# 	outroFrames
	# ))

	# # place the pause-sequence into the queue
	# queue.put((
	# 	'pause.svg',
	# 	'pause.dv',
	# 	pauseFrames
	# ))
