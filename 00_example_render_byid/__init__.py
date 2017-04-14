#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://2016.mrmcd.net/fahrplan/schedule.xml'

def introFrames(args):
#fade in pillgroup0
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('pillgroup0', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('pillgroup1', 'style', 'opacity', 0),
            ('pillgroup2', 'style', 'opacity', 0),
            ('pillgroup3', 'style', 'opacity', 0),
            ('pillgroup4', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
#fade in and move in pillgroup 1-4 of thorax + fade in logotext
    y12start = 1450
    y12end = 917.679
    x3start = 610
    x4start = 610
    frames = 2*fps
    for i in range(0, frames):
        y12 = (y12end-y12start) - ((i+1) * ((y12end-y12start)/frames))
        x3 = -x3start + ((i+1) * (x3start/frames))
        x4 = x4start - ((i+1) * ((x4start)/frames))
        #print("---------------------------------------------------")
        #print (i, "/", frames)
        #print(y12)
        #print(x3)
        #print(x4)
        #print("---------------------------------------------------")
        yield (
            ('pillgroup1', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('pillgroup2', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('pillgroup3', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('pillgroup4', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('logotext', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('pillgroup1', 'attr', 'transform', 'translate(0, %.4f)' % (y12)),
            ('pillgroup2', 'attr', 'transform', 'translate(0, %.4f)' % (y12)),
            ('pillgroup3', 'attr', 'transform', 'translate(%.4f, 0)' % (x3)),
            ('pillgroup4', 'attr', 'transform', 'translate(%.4f, 0)' % (x4)),
        )
#show pillgroup 0-4 + logotext for 1 second
    frames = 1*fps
    for i in range(0, frames):
        yield(
            ('pillgroup0', 'style', 'opacity', 1),
            ('pillgroup1', 'style', 'opacity', 1),
            ('pillgroup2', 'style', 'opacity', 1),
            ('pillgroup3', 'style', 'opacity', 1),
            ('pillgroup4', 'style', 'opacity', 1),
            ('logotext', 'style', 'opacity', 1),
        )
#move pillgroup 0-4 + logotext to right
    frames = 2*fps
    for i in range(0, frames):
        xshift = (i+1) * 490/frames
        #print(xshift)
        yield(
            ('pillgroup0', 'attr', 'transform', 'translate(%.4f, 0)' % (xshift)),
            ('pillgroup1', 'attr', 'transform', 'translate(%.4f, 0)' % (xshift)),
            ('pillgroup2', 'attr', 'transform', 'translate(%.4f, 0)' % (xshift)),
            ('pillgroup3', 'attr', 'transform', 'translate(%.4f, 0)' % (xshift)),
            ('pillgroup4', 'attr', 'transform', 'translate(%.4f, 0)' % (xshift)),
            ('logotext', 'attr', 'transform', 'translate(%.4f, 0)' % (xshift)),
        )
#fade in title, subtitle, persons and id
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('subtitle', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('id', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )
#show whole image for 2 seconds
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('subtitle', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('id', 'style', 'opacity', 1),
        )

def backgroundFrames(parameters):
    # 40 Sekunden

        frames = 20*fps
        for i in range(0, frames):
            xshift = (i+1) * 300/frames
            yshift = ((i+1) * (150/frames))
            yield(
                        ('pillgroup', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
            )

        frames = 20*fps
        for i in range(0, frames):
            xshift = 300 - ((i+1) * (300/frames))
            yshift = 150 - ((i+1) * (150/frames))
            yield(
                        ('pillgroup', 'attr', 'transform', 'translate(%.4f, %.4f)' % (xshift, yshift)),
            )

def outroFrames(args):
#fadein outro graphics
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('pillgroup', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('logotext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('c3voclogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('c3voctext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysalogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysatext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('pillgroup', 'style', 'opacity', 1),
            ('logotext', 'style', 'opacity', 1),
            ('c3voclogo', 'style', 'opacity', 1),
            ('c3voctext', 'style', 'opacity', 1),
            ('bysalogo', 'style', 'opacity', 1),
            ('bysatext', 'style', 'opacity', 1),
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
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'StageWar live!',
            '$subtitle': 'Metal Konzert',
            '$persons':  'www.stagewar.de'
        }
    )

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


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if 000000 in idlist:
            continue
        if event['room'] not in ('Chirurgie (Saal 1.04)', 'Kreißsaal (Saal 1.11)'):
            print("skipping room %s (%s)" % (event['room'], event['title']))
            continue
        if not (idlist==None):
            if int(event['id']) not in idlist:
                print("skipping id %s (%s)" % (event['id'], event['title']))
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

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile = 'background.svg',
            outfile = 'background.ts',
            sequence = backgroundFrames
        ))
