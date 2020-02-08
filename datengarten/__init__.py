#!/usr/bin/python3

from renderlib import *
from easing import *

scheduleUrl = "https://berlin.ccc.de/datengarten/index.xml"

personmap = {
}

taglinemap = {
}


def introFrames(p):
	move=50

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
		yield ()

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
			'$id': 69,
			'$title': 'Ethik des Digitalen',
			'$person': 'Daniel Domscheit-Berg'
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Saal23'):
            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            continue
        if not (idlist==[]):
            if 000000 in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue
            if int(event['id']) not in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue

    # generate a task description and put it into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['subtitle'],
                '$person': event['personnames']
                }
            ))

        for person in persons(scheduleUrl, personmap, taglinemap, event['id']):
            queue.put(Rendertask(
                infile = 'lower-third.svg',
                outfile = 'event_{}_person_{}.png'.format(str(event['id']), str(person['id'])),
                parameters = {
                    '$PERSON': person['person'],
                    '$TAGLINE': person['tagline'],
                    }
                ))

        queue.put(Rendertask(
            infile = 'lower-third.svg',
            outfile = 'event_{}_persons.png'.format(str(event['id'])),
            parameters = {
                '$PERSON': event['personnames'],
                '$TAGLINE': '',
                }
            ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

