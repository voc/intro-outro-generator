#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

scheduleUrl = ""

def introFrames(p):
        # 8 Sekunden

        # 2 Sekunden Fadein logo
        frames = int(2*fps)
        for i in range(0, frames):
                yield (
                        ('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
                        ('text',  'style',    'opacity', 0),
                )

        # 3 Sekunden Fadein text
        frames = 3*fps
        for i in range(0, frames):
                yield (
                        ('logo',  'style',    'opacity', 1),
                        ('text',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
                )

        # 3 Sekunden stehen bleiben
        frames = 3*fps
        for i in range(0, frames):
                yield (
                        ('logo',  'style',    'opacity', 1),
                        ('text',  'style',    'opacity', 1),
                )

def outroFrames(p):
        # 8 Sekunden

        # 1 Sekunden stehen bleiben
        frames = int(1*fps)
        for i in range(0, frames):
                yield (
                        ('logo',  'style',    'opacity', 1),
                )

        # 4 Sekunde Fadeout Logo
        frames = 4*fps
        for i in range(0, frames):
                yield (
                        ('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 1, -1, frames)),
                )

        # 1 Sekunden stehen bleiben
        frames = 1*fps
        for i in range(0, frames):
                yield (
                        ('logo',  'style',    'opacity', 0),
                )


def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': '246',
			'$title': 'Die Gesellschaft für Freiheitsrechte',
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)


def tasks(queue, args, idlist, skiplist):
    if scheduleXml == "":
        raise "Not schedule yet, use --debug for now"

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

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

