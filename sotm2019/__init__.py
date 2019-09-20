#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://sotm.osmz.ru/19.xml'

def introFrames(args):
#fade in tux and set other opacities to 0
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
        )

#fade in title and persons
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )

#show whole image for 5 seconds
    frames = 5*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
        )



def outroFrames(args):
#fadein outro graphics
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('tux', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('cctext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('logo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('tux', 'style', 'opacity', 1),
            ('cctext', 'style', 'opacity', 1),
            ('logo', 'style', 'opacity', 1),
        )


def debug():
    render(
      'intro.svg',
      '../intro.ts',
      introFrames,
      {
          '$title': "Long Long Long title is LONG",
          '$speaker': 'Long Name of Dr. Dr. Prof. Dr. Long Long'
      }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Hörsaal Ost', 'Großer Hörsaal', 'Hörsaal West'):
            print("skipping room %s (%s)" % (event['room'], event['title']))
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
                '$title': event['title'],
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

