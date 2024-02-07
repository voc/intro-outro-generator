#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://data.c3voc.de/afu-tm18/schedule-afu-tm18.xml'

# For (really) too long titles
titlemap = {
}

def introFrames(p):
	move=50

	# 1/2 Sekunden stehen lassen
	frames = 12
	for i in range(0, frames):
		yield (
			('text', 'style',    'opacity', "%.4f" % 0),
			('text', 'attr',     'transform', 'translate(%.4f, 0)' % 0),
		)

	# 3 Sekunde Text Fadein
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('text', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
			('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, -move, move, frames)),
		)

	# 2 Sekunden stehen lassen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text', 'style',    'opacity', "%.4f" % 1),
			('text', 'attr',     'transform', 'translate(%.4f, 0)' % 0),
		)

	# 3 Sekunde Text Fadeout
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('text', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
			('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeInQuad(i, 0, move, frames)),
		)

	# two final frames
	for i in range(0, 2):
		yield (
			('text', 'style',    'opacity', "%.4f" % 0),
			('text', 'attr',     'transform', 'translate(%.4f, 0)' % move),
		)

def outroFrames(p):
	# 5 Sekunden stehen bleiben
	frames = 5*fps
	for i in range(0, frames):
		yield ()

def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': 1002,
			'$title': 'Die Fakultät für Elektrotechnik und Informationstechnik stellt sich vor',
			'$person': 'Prof. Hiebel'
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

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
                                '$person': event['personnames']
                        }
                ))

        # place a task for the outro into the queue
        queue.put(Rendertask(
                infile = 'outro.svg',
                outfile = 'outro.ts',
                sequence = outroFrames
        ))
