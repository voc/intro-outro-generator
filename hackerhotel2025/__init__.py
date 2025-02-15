#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://pretalx.hackerhotel.nl/2025/schedule/export/schedule.xml'

def bounce(i, min, max, frames):
    if i == frames - 1:
        return 0

    if i <= frames/2:
        return easeInOutQuad(i, min, max, frames/2)
    else:
        return max - easeInOutQuad(i - frames/2, min, max, frames/2)

def introFrames(parameters):
    # 1 Sekunde Text Fadein
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
        )

    # 4 Sekunden stehen lassen
    frames = 4*fps
    for i in range(0, frames):
        yield ()

    # 1 Sekunde Fade to black layer
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('all', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
        )

def pauseFrames(parameters):
    #5 Seconds Fade-In Hacker Fade-Out Hotel
    frames = 5*fps
    for i in range(0, frames):
        yield (
            ('logohacker', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
            ('logohotel', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
        )
    #5 Seconds Fade-In Hotel Fade-Out Hacker
    frames = 5*fps
    for i in range(0, frames):
        yield (
            ('logohacker', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
            ('logohotel', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
        )

def outroFrames(p):
    # 4 Sekunden stehen bleiben
    frames = 4*fps
    for i in range(0, frames):
        yield []
    # 1 Sekunde Fade to black layer
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('all', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
        )

def debug():
    render(
      'intro.svg',
      '../intro.ts',
      introFrames,
      {
          '$ID': 4711,
          '$TITLE': "Long Long Long title is LONG",
          '$SUBTITLE': 'Long Long Long Long subtitle is LONGER',
          '$SPEAKER': 'Long Name of Dr. Dr. Prof. Dr. Long Long'
      }
    )

    render(
        'pause.svg',
        '../pause.ts',
        pauseFrames
    )

#    render(
#        'infobeamer.svg',
#        '../infobeamer.ts',
#        pauseFrames
#    )

    render(
      'outro.svg',
      '../outro.ts',
      outroFrames
    )

def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Leonardo Da Vinci', 'Mission Critical Room (Rembrandt)', 'Willem van Oranje'):
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
                '$ID': event['id'],
                '$TITLE': event['title'],
                '$SUBTITLE': event['subtitle'],
                '$SPEAKER': event['personnames']
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
