#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://import.c3voc.de/schedule/realraum.xml?showall=yes'

def introFrames(args):
    frames = int(0.5 * fps)
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('header', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('logo_group', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )

    # fade in title, subtitle, persons and id
    frames = 1 * fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )

    # show whole image for 4 seconds
    frames = 4 * fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('subtitle', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('id', 'style', 'opacity', 1),
        )

def outroFrames(args):
    # fadein outro graphics
    frames = 1 * fps
    for i in range(0, frames):
        yield(
            ('black', 'style', 'opacity', 0),
            ('header', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('logo_group', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )

    frames = 3 * fps
    for i in range(0, frames):
        yield(
            ('header', 'style', 'opacity', 1),
            ('logo_group', 'style', 'opacity', 1),
        )

    # fade to black
    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('black', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )

def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'StageWar live!',
            '$subtitle': 'Metal Konzert',
            '$persons':  'www.stagewar.de'
        }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    if not "intro" in skiplist:
        for event in events(scheduleUrl):
            if not (idlist==[]):
                    if 000000 in idlist:
                            print("skipping id (%s [%s])" % (event['title'], event['id']))
                            continue
                    if int(event['id']) not in idlist:
                            print("skipping id (%s [%s])" % (event['title'], event['id']))
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
                    '$persons': event['personnames']
                }
            ))

    # place a task for the outro into the queue
    if not "out" in skiplist and idlist==[]:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))
