#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://live.ber.c3voc.de/releases/public/schedule.xml'

# For (really) too long titles
titlemap = {
    #
}

def bounce(i, min, max, frames):
    if i == frames - 1:
        return 0

    if i <= frames/2:
        return easeInOutQuad(i, min, max, frames/2)
    else:
        return max - easeInOutQuad(i - frames/2, min, max, frames/2)

def introFrames(parameters):
    move=50

    # 3 Sekunde Text Fadein
    frames = 3*fps
    for i in range(0, frames):
        yield (
            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
            ('textblock', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, -move, move, frames)),
        )

    # 2 Sekunden stehen lassen
    frames = 2*fps
    for i in range(0, frames):
        yield ()

    # 3 Sekunde Text Fadeout
    frames = 3*fps
    for i in range(0, frames):
        yield (
            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
            ('textblock', 'attr',     'transform', 'translate(%.4f, 0)' % easeInQuad(i, 0, move, frames)),
        )

def pauseFrames(parameters):
    frames = 25*3
    for i in range(0, frames):
        yield (
            ('pause', 'attr', 'flood-opacity', '%.4f' % bounce(i, 0.0, 1.0, frames)),
        )

    frames = 25*1
    for i in range(0, frames):
        yield (
            ('glowFlood', 'attr', 'flood-opacity', '%.4f' % 0),
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

def tasks(queue, args):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):

        if len(args) > 0:
            if not str(event['id']) in args:
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
