#!/usr/bin/python3


from renderlib import *
from easing import *
from collections import deque

scheduleUrl = 'https://live.ber.c3voc.de/releases/kolo/schedule.xml'

# For (really) too long titles
titlemap = {
}

def introFrames(parameters):
	# 8 Sekunden

	frames = int(1*fps)
	for i in range(0, frames):
		yield (
			('black',  'style',    'opacity', "%.4f" % easeInOutQuart(i, 1, -1, frames)),
		)

	frames = 6*fps
	for i in range(0, frames):
		yield (
			('black',  'style',    'opacity', "%.4f" % 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('black',  'style',    'opacity', "%.4f" % easeInOutQuart(i, 0, 1, frames)),
		)

def outroFrames(parameters):
	# 5 Sekunden
	frames = 4*fps
	for i in range(0, frames):
		yield (
			('black',  'style',    'opacity', "%.4f" % 0),
		)

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('black',  'style',    'opacity', "%.4f" % easeInOutQuart(i, 0, 1, frames)),
		)

def debug():
	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

	s1 = 'Lorem, Ipsum, Ad Dolor... '
	s2 = 'Lorem, Ipsum, Ad Dolor, Sit, Nomen, Est, Omen, Urbi et Orbi... '
#	render(
#		'intro.svg',
#		'../intro.ts',
#		introFrames,
#		{
#                    '$title': s1,
#                    '$personnames': s2
#
#		}
#	)
#

def tasks(queue, args, idlist, skip):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if not (idlist==[]):
			if 000000 in idlist:
				print("skipping id (%s [%s])" % (event['title'], event['id']))
				continue
			if int(event['id']) not in idlist:
				print("skipping id (%s [%s])" % (event['title'], event['id']))
				continue
		# generate a task description and put them into the queue
		projectname = event['title']
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
				'$title': event['title'],
				'$personnames': event['personnames']
			}
		))

	# place a task for the outro into the queue
	queue.put(Rendertask(
		infile = 'outro.svg',
		outfile = 'outro.ts',
		sequence = outroFrames
	))

