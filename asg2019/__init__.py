#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://cfp.all-systems-go.io/ASG2019/schedule/export/schedule.xml'

# For (really) too long titles
titlemap = {
#    72: "Maximize your creativity and quality of use of HMI for automotive. TRITO Linkage, a compre-hensive HMI tool chain for Qt."
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

    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('speaker', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
        )

    # 3 Sekunde Text Fadeout
    frames = 4*fps
    for i in range(0, frames):
        yield []

def pauseFrames(parameters):
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('pause',   'attr', 'opacity', '%.4f' % easeLinear(i, 0, 1, frames)),
            ('details', 'attr', 'opacity', '%.4f' % easeLinear(i, 1, -1, frames)),
        )
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('pause',   'attr', 'opacity', '1'),
            ('details', 'attr', 'opacity', '0'),
        )
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('pause',   'attr', 'opacity', '%.4f' % easeLinear(i, 1, -1, frames)),
            ('details', 'attr', 'opacity', '%.4f' % easeLinear(i, 0, 1, frames)),
        )
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('pause',   'attr', 'opacity', '0'),
            ('details', 'attr', 'opacity', '1'),
        )

def outroFrames(p):
    # 2 Sekunden stehen bleiben
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('sponsoredby',   'style',    'opacity', "1"),
            ('recordedby',    'style',    'opacity', "0"),
            ('cc',            'style',    'opacity', "0"),
        )
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('sponsoredby',   'style',    'opacity', "%.4f" % easeInOutQuad(i, 1, -1, frames)),
            ('recordedby',    'style',    'opacity', "%.4f" % easeInOutQuad(i, 0, 1, frames)),
            ('cc',            'style',    'opacity', "0"),
        )
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('sponsoredby',   'style',    'opacity', "0"),
            ('recordedby',    'style',    'opacity', "1"),
            ('cc',            'style',    'opacity', "0"),
        )
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('sponsoredby',   'style',    'opacity', "0"),
            ('recordedby',   'style',    'opacity', "%.4f" % easeInOutQuad(i, 1, -1, frames)),
            ('cc',           'style',    'opacity', "%.4f" % easeInOutQuad(i, 0, 1, frames)),
        )
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('sponsoredby',   'style',    'opacity', "0"),
            ('recordedby',    'style',    'opacity', "0"),
            ('cc',            'style',    'opacity', "1"),
        )

def backgroundFrames(parameters):
    return
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

        frames = 20*fps
        for i in range(0, frames):
            xshift = 300 - ((i+1) * (300/frames))
            yshift = 150 - ((i+1) * (150/frames))
            yield(
                        ('pillgroup', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
            )

def debug():
    render(
      'intro.svg',
      '../intro.ts',
      introFrames,
      {
          '$ID': 4711,
          '$TITLE': "Long Long Long title is LONG",
          '$COMPANY': 'Long Running Co',
          '$SPEAKER': 'Dr. Dr. Prof. Dr. Long Long'
      }
    )

#    render(
#        'pause.svg',
#        '../pause.ts',
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
        #if event['room'] not in ('Galerie', 'Saal (Main Hall)'):
        #    print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
        #    continue
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
                '$COMPANY': event['subtitle'],
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

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile = 'background.svg',
            outfile = 'background.ts',
            sequence = backgroundFrames
        ))
