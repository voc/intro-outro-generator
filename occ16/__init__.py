#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://2016.mrmcd.net/fahrplan/schedule.xml'

##intro done with seperate script by danimo

def backgroundFrames(parameters):
    # 80 Sekunden

        frames = 40*fps
        for i in range(0, frames):
            xshift = (i+1) * 300/frames
            yshift = ((i+1) * (150/frames))
            yield(
                        ('movingbg', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
            )

        frames = 40*fps
        for i in range(0, frames):
            xshift = 300 - ((i+1) * (300/frames))
            yshift = 150 - ((i+1) * (150/frames))
            yield(
                        ('movingbg', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
            )

def outroFrames(args):
#fadein outro graphics
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('logogroup', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('c3voclogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('c3voctext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysalogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysatext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('logogroup', 'style', 'opacity', 1),
            ('c3voclogo', 'style', 'opacity', 1),
            ('c3voctext', 'style', 'opacity', 1),
            ('bysalogo', 'style', 'opacity', 1),
            ('bysatext', 'style', 'opacity', 1),
        )

def pauseFrames(args):
#fade heartgroups
        frames = int(2*fps)
        for i in range(0, frames):
                yield (
                        ('oclogo', 'style', 'opacity', easeInQuad(i, 0.1, 1, frames)),
                        ('breaktext', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
                )
        frames = int(2*fps)
        for i in range(0, frames):
                yield (
                        ('oclogo', 'style', 'opacity', easeInQuad(i, 1,-1, frames)),
                        ('breaktext', 'style', 'opacity', easeInQuad(i, 0.1, 1, frames)),
                )

def debug():
    render('outro.svg',
        '../outro.ts',
        outroFrames
    )

    render(
        'background.svg',
        '../background.ts',
        backgroundFrames
    )

    render('pause.svg',
        '../pause.ts',
        pauseFrames
    )


def tasks(queue, args):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Chirurgie (Saal 1.04)', 'Kreißsaal (Saal 1.11)'):
            print("skipping room %s (%s)" % (event['room'], event['title']))
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
    queue.put(Rendertask(
        infile = 'outro.svg',
        outfile = 'outro.ts',
        sequence = outroFrames
    ))

    # place the pause-sequence into the queue
    queue.put(Rendertask(
        infile = 'pause.svg',
        outfile = 'pause.ts',
        sequence = pauseFrames
    ))

    # place the pause-sequence into the queue
    queue.put(Rendertask(
        infile = 'background.svg',
        outfile = 'background.ts',
        sequence = backgroundFrames
    ))
