#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from easing import *
import svg.path

# URL to Schedule-XML
scheduleUrl = 'https://talks.2019.foss4g.org/bucharest/schedule/export/schedule.xml'

# For (really) too long titles
titlemap = {
        198: 'Revamp of CRS management in the OSGeo C/C++ stack with PROJ and GDAL',
}


def introFrames(args):
    #1 Sec Background
    frames = 1*fps
    for i in range(0,frames):
        yield(
            ('text', 'style', 'opacity', 0),
            ('image1105', 'style', 'opacity', 1),
        )

    #2 Sec FadeIn Text
    frames = 2*fps
    for i in range(0,frames):
        yield(
            ('text', 'style', 'opacity', "%.4f" % easeInCubic(i,0,1,frames)),
            ('image1105', 'style', 'opacity', 1),
        )

    #4 Sec Everything
    frames = 4*fps
    for i in range(0,frames):
        yield(
            ('text', 'style', 'opacity', 1),
            ('image1105', 'style', 'opacity', 1),
        )


def outroFrames(args):
    # 5 Sec everything
    frames = 5*fps
    for i in range(0,frames):
        yield(
            ('layer1', 'style', 'opacity', 1),
            ('layer2', 'style', 'opacity', 1),
        )

def pauseFrames(params):
        # 2 sec Fadein Text1
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                        ('text2', 'style', 'opacity', 0),
                )

    # 2 sec Text1
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', 1),
                        ('text2', 'style', 'opacity', 0),
                )

        # 2 sec Fadeout Text1
        frames = 2*fps
        for i in range(0, frames):
            yield (
                        ('text1', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
                        ('text2', 'style', 'opacity', 0),
                )

        # 2 sec blank
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', 0),
                        ('text2', 'style', 'opacity', 0),
                )

        # 2 sec Fadein Text2
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text2', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                        ('text1', 'style', 'opacity', 0),
                )


        # 2 sec Text2
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text2', 'style', 'opacity', 1),
                        ('text1', 'style', 'opacity', 0),
                )

        # 2 sec Fadeout Text2
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text2', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
                        ('text1', 'style', 'opacity', 0),
                )

        # 2 sec blank
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', 0),
                        ('text2', 'style', 'opacity', 0),
                )
    
def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 2404,
            '$title': 'Linux Container im High Performance Computing',
            '$subtitle': 'Vom Wal zur Singularität und weiter',
            '$personnames': 'Holger Gantikow'
        }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Plenary (National Theatre)', 'Ronda Ballroom', 'Fortuna West', 'Fortuna East', 'Rapsodia Ballroom', 'Opera Room', 'Opereta Room', 'Simfonia','Menuet','Hora Room','Coral Room'):
            print("skipping room %s (%s)" % (event['room'], event['title']))
            continue

        if (event['id'] in idlist or not idlist) and not 'intro' in skiplist:
        # generate a task description and put them into the queue
            queue.put(Rendertask(
                infile = 'intro.svg',
                outfile = str(event['id'])+".ts",
                sequence = introFrames,
                parameters = {
                    '$id': event['id'],
                    '$title': event['title'] if event['id'] not in titlemap else titlemap[event['id']],
                    '$subtitle': event['subtitle'],
                    '$personnames': event['personnames']
                }
            ))

    if not 'outro' in skiplist:
        # place a task for the outro into the queue
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
        ))

    if not 'pause' in skiplist:
        # place a task for the pause into the queue
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
        ))
