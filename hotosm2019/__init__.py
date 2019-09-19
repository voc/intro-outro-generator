#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://summit2019.hotosm.org/schedule.xml'

def introFrames(args):
    # show logo first for 2 seconds
    frames = 4*fps
    for i in range(0, frames):
        yield (
            ('logo-artwork', 'style', 'opacity', 1),
            ('talk-metadata', 'style', 'opacity', 1),
        )
#    # show title, subtitle and speakers for 3 seconds
#    frames = 3*fps
#    for i in range(0, frames):
#        yield (
#            ('logo-artwork', 'style', 'opacity', 0),
#            ('talk-metadata', 'style', 'opacity', 1),
#        )

#def backgroundFrames(parameters):
#    # 40 Sekunden
#
#        frames = 20*fps
#        for i in range(0, frames):
#            xshift = (i+1) * 300/frames
#            yshift = ((i+1) * (150/frames))
#            yield(
#                        ('pillgroup', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
#            )
#
#        frames = 20*fps
#        for i in range(0, frames):
#            xshift = 300 - ((i+1) * (300/frames))
#            yshift = 150 - ((i+1) * (150/frames))
#            yield(
#                        ('pillgroup', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
#            )

def outroFrames(args):
#fadein outro graphics
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('everything', 'style', 'opacity', "%.4f" % easeInQuad(i, 0.01, 1, frames)),
        )
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('everything', 'style', 'opacity', 1),
        )

def pauseFrames(args):
        frames = int(3*fps) + 1
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', "%.4f" % easeInQuad(i, 0.0, 1.0, frames)),
                )
        frames = int(3*fps)
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', 1.0),
                )
        frames = int(3*fps)
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', "%.4f" % easeOutQuad(i, 0.0, 1.0, frames)),
                )
        frames = int(3*fps)
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', 0),
                )

def debug():
#    render('intro.svg',
#        '../intro.ts',
#        introFrames,
#        {
#            '$id': 7776,
#            '$title': 'StageWar live!',
#            '$subtitle': 'Metal Konzert',
#            '$persons':  'www.stagewar.de'
#        }
#    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )

#    render(
#        'background.svg',
#        '../background.ts',
#        backgroundFrames
#    )
#
    render('pause.svg',
        '../pause.ts',
        pauseFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Chirurgie (Saal 1.04)', 'Kreißsaal (Saal 1.11)'):
            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            continue
        if not (idlist==[]):
                if 000000 in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue
                if int(event['id']) not in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
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

#    # place the background-sequence into the queue
#    if not "bg" in skiplist:
#        queue.put(Rendertask(
#            infile = 'background.svg',
#            outfile = 'background.ts',
#            sequence = backgroundFrames
#        ))
