#!/usr/bin/python3

from renderlib import *
import math

# URL to Schedule-XML
scheduleUrl = 'https://fahrplan.bits-und-baeume.org/schedule.xml'

# For (really) too long titles
titlemap = {
	#708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}

def easeInCubic(t, b, c, d):
	t=float(t)/d
	return c*(t)*t*t + b;

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

	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	frames = math.ceil(3.5*fps)
	for i in range(0, frames):
		yield (
			('text',  'style',    'opacity', 1),
		)

def pauseFrames(p):
	pass


def tasks(queue, params, idlist, skiplist):
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
		if int(event['id']) not in skiplist:
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
	if not "out" in skiplist:
		queue.put(Rendertask(
			infile = 'outro.svg',
			outfile = 'outro.ts',
			sequence = outroFrames
		))

	# # place the pause-sequence into the queue
	# queue.put(Rendertask(
	# 	infile = 'pause.svg',
	# 	outfile = 'pause.ts',
	# 	sequence = pauseFrames
	# ))
