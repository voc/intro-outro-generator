#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://cfp.gulas.ch/gpn20/schedule/export/schedule.xml'

def introFrames(args):
    for frame in range(0, fps):
        yield (
            ('title', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('gfactoryreset', 'style', 'opacity', 0),
            *((f'g{i}', 'style', 'opacity', int(i<=frame)) for i in range(0,26))
        )



#fade in title and persons
    frames = 1*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('gfactoryreset', 'style', 'opacity', 1),
            *((f'g{i}', 'style', 'opacity', 1) for i in range(0,26))
        )

#show whole image for 5 seconds
    frames = 5*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('gfactoryreset', 'style', 'opacity', 1),
            *((f'g{i}', 'style', 'opacity', 1) for i in range(0,26))
        )

    frames = 1*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            ('persons', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            ('gfactoryreset', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            *((f'g{g}', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)) for g in range(0,26))
        )


def outroFrames(args):
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('cc-text', 'style', 'opacity', 1),
            ('logo', 'style', 'opacity', 1),
        )
    #fadeout outro graphics
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('cc-text', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            ('logo', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
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
        if event['room'] not in ('Medientheater', "Vortragssaal", "Blauer Salon", "Ausstellung BioMedien"):
            print("skipping room %s (%s)" % (event['room'], event['title']))
            continue
        if event['day'] not in ('1', '2', '3', '4'):
            print("skipping day %s" % (event['day']))
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

