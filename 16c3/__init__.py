#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://live.ber.c3voc.de/releases/schedules/16c3_schedule.xml'

# For (really) too long titles
titlemap = {
    #
}

def introFrames(parameters):
    move=50

    # 3 Sekunde Text Fadein
    frames = 3*fps
    for i in range(0, frames):
        yield (
            ('logo', 'style',    'opacity', "%.4f" % easeInQuad(min(i*2,frames), 0, 1, frames)),
            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
            ('textblock', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, -move/2, move/2, frames)),
        )

    # 2 Sekunden stehen lassen
    frames = 2*fps
    for i in range(0, frames):
        yield ()

    # 3 Sekunde Text Fadeout
    frames = 3*fps
    for i in range(0, frames):
        yield (
#            ('textblock', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
#            ('textblock', 'attr',     'transform', 'translate(%.4f, 0)' % easeInQuad(i, 0, move, frames)),
            ('fadebg', 'style',    'opacity', "%.4f" % easeInOutQuad(min(i*2,frames), 0, 1, frames)),
        )

def pauseFrames(parameters):
    pass

def outroFrames(p):
    # 5 Sekunden stehen bleiben
    frames = 5*fps
    for i in range(0, frames):
        yield []

def debug():
    render(
      'intro.svg',
      '../intro.dv',
      introFrames,
      {
          '$id': 4711,
          '$title': "Long Long Long title is LONG",
          '$personnames': 'Long Name of Dr. Dr. Prof. Dr. Long Long'
      }
    )

#    render(
#        'pause.svg',
#        '../pause.dv',
#        pauseFrames
#    )
#
    render(
      'outro.svg',
      '../outro.dv',
      outroFrames
    )

def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):

#        if len(args) > 0:
#            if not str(event['id']) in args:
#                continue
        # generate a task description and put it into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".dv",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$personnames': event['personnames']
                }
            ))
