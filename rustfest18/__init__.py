#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://team.rrbone.net/public/rustfest18.xml'

def introFrames(args):
#fade in pillgroup0
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('logotext', 'style', 'opacity', 0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
#fade in title, subtitle, persons and id
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('subtitle', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('id', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )
#show whole image for 2 seconds
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('subtitle', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('id', 'style', 'opacity', 1),
        )

def outroFrames(args):
#fadein outro graphics
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('background', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('rrbonelogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('c3voclogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('c3voctext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysalogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysatext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('background', 'style', 'opacity', 1),
            ('rrbonelogo', 'style', 'opacity', 1),
            ('c3voclogo', 'style', 'opacity', 1),
            ('c3voctext', 'style', 'opacity', 1),
            ('bysalogo', 'style', 'opacity', 1),
            ('bysatext', 'style', 'opacity', 1),
        )

def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Auditorium'):
            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            continue
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
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))
