#!/usr/bin/python

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://live.ber.c3voc.de/releases/suselabs18/schedule.xml'

def bounce(i, min, max, frames):
    if i == frames - 1:
        return 0

    if i <= frames/2:
        return easeInOutQuad(i, min, max, frames/2)
    else:
        return max - easeInOutQuad(i - frames/2, min, max, frames/2)

def introFrames(parameters):
    # 3 Sekunde Text Fadein
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
            ('fadeout', 'style',    'opacity', "%.4f" % 0),
        )

    # 4 Sekunden stehen lassen
    frames = 4*fps
    for i in range(0, frames):
        yield (
            ('fadeout', 'style',    'opacity', "%.4f" % 0),
        )

    # 1 Sekunde Fade to black layer
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('fadeout', 'style',    'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
        )

def pauseFrames(parameters):
    frames = 3*fps
    colors = ['#21A4D4', '#73BA25', '#6DA741', '#35B9AB', '#00A489', '#173F4F']
    yield (
        ('pause_bg', 'style', 'fill', "%s" % '#173F4F'),
        ('pause_bg', 'attr', 'opacity', '%.4f' % 1.0),
    )
    for i in range(0, len(colors)):
        z = 0
        for z in range(0,frames):
            yield (
                ('pause_bg_alt', 'style', 'fill', "%s" % colors[i]),
                ('pause_bg_alt', 'attr', 'opacity', '%.4f' % easeLinear(z, 0.0, 1.0, frames)),
            )
        yield (
            ('pause_bg', 'style', 'fill', "%s" % colors[i]),
            ('pause_bg', 'attr', 'opacity', '%.4f' % 1.0),
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

    render(
      'outro.svg',
      '../outro.ts',
      outroFrames
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
