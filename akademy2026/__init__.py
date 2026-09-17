#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://data.c3voc.de/kde2026/schedule.xml'

def outroFrames(args):
#fadein outro graphics
    frames = int(0.6*fps)
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bottom_text', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysalogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysatext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )
    frames = int(4.4*fps)
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', 1),
            ('bottom_text', 'style', 'opacity', 1),
            ('bysalogo', 'style', 'opacity', 1),
            ('bysatext', 'style', 'opacity', 1),
        )

    frames = int(0.6 * fps)
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            ('bottom_text', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            ('bysalogo', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
            ('bysatext', 'style', 'opacity', easeOutQuad(i, 1, -1, frames)),
        )

def pauseFrames(args):
#fade heartgroups
        frames = int(0.5*fps)
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 0.25, 0.75, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('heartgroup1', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup2', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                        ('heartgroup3', 'style', 'opacity', easeInQuad(i, 1, -0.75, frames)),
                )

def debug():
    render('outro.svg',
        '../outro.ts',
        outroFrames
    )

    render('pause.svg',
        '../pause.ts',
        pauseFrames
    )


def tasks(queue, args, idlist, skiplist):
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

