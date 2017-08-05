#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://c3voc.de/share/schedules/mm17.xml'

def introFrames(args):
#show for 1 second
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('persons2', 'style', 'opacity', 0),
        )

#fade in 2 seconds
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons2', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )

#show for 5 seconds
    frames = 5*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('persons2', 'style', 'opacity', 1),
        )

def backgroundFrames(arg):
#show for 1 second
    frames = 1*fps
    for i in range(0, frames):
        yield tuple()

def outroFrames(args):
# show for 6 seconds
    frames = 6*fps
    for i in range(0, frames):
        yield tuple()

def pauseFrames(args):
# show for 1 second
    frames = 1*fps
    for i in range(0, frames):
        yield tuple()

def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$title': 'Make Munich Vortag',
            '$persons1': 'MM17 1',
            '$persons2': 'MM17 2'
        }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )

    render(
        'background.svg',
        '../background.ts',
        backgroundFrames
    )

    render('pause.svg',
        '../pause.ts',
        pauseFrames
    )


def tasks(queue, args, idlist, skiplist):
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
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$persons1': event['personnames'].upper(),
                '$persons2': event['personnames2'].upper()
            }
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

    # place the pause-sequence into the queue
    if not "pause" in skiplist:
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
        ))

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile = 'background.svg',
            outfile = 'background.ts',
            sequence = backgroundFrames
        ))
