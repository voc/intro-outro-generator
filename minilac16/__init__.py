#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *
from lxml import etree

# URL to Schedule-XML
scheduleUrl = 'https://live.dus.c3voc.de/lac16/schedule.xml'

def introFrames(p):
	move=50

	# 4 Sekunden stehen lassen
	frames = 2*fps
	for i in range(0, frames):
                yield (
			('text', 'style',    'opacity', "%.4f" % 100),
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
		yield []

def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': 2,
			'$title': 'Essential Aspects on Mixing',
			'$person': 'Jimson Drift'
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

def tasks(queue, args):
	raise NotImplementedError('call with --debug to render your intro/outro')
def tasks(queue, args):
        # iterate over all events extracted from the schedule xml-export
        for event in events(scheduleUrl):
                if event['room'] not in ('Seminar room', 'Soundlab', 'Mainhall'):
                        print("skipping room %s (%s)" % (event['room'], event['title']))
                        continue

                # generate a task description and put them into the queue
                queue.put(Rendertask(
                        infile = 'intro.svg',
                        outfile = str(event['id'])+".ts",
                        sequence = introFrames,
                        parameters = {
                                '$id': event['id'],
                                '$title': event['title'],
                                '$subtitle': event['subtitle'],
                                '$person': event['personnames']
                        }
                ))

        # place a task for the outro into the queue
        queue.put(Rendertask(
                infile = 'outro.svg',
                outfile = 'outro.ts',
                sequence = outroFrames
        ))
