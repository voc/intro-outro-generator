#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://cfp.owncloud.com/occon18/schedule/export?exporter=core-frab-xml'

def introFrames(args):
#fade in logo
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', easeInQuad(i, 0, 1.5, frames)),
            ('confname', 'style', 'opacity', easeInQuad(i, 0, 1.25, frames)),
            ('confdate', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
#fade in title, subtitle, person and id
    frames = 4*fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', 1),
            ('confname', 'style', 'opacity', 1),
            ('confdate', 'style', 'opacity', 1),
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('subtitle', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('id', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )
#show whole image
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('subtitle', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('id', 'style', 'opacity', 1),
        )

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
#fade logo + pause
        frames = int(2*fps)
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', easeInQuad(i, 0.1, 1, frames)),
                        ('pause', 'style', 'opacity', easeInQuad(i, 1, -0.9, frames)),
                )
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', easeInQuad(i, 1, -0.9, frames)),
                        ('pause', 'style', 'opacity', easeInQuad(i, 0.1, 1, frames)),
                )

def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': '23',
            '$title': 'Performance testing of OwnCloud using VirtualBox and Apache JMeter',
            '$subtitle': 'Foo Bar Foo Bar Foo Bar Foo Bar Foo Bar Foo Bar Foo Bar Foo Bar',
            '$persons':  'Jean-Marie de Boer,  Jean-Marie de Boer,  Jean-Marie de Boer'
        }
    )

#    render('outro.svg',
#        '../outro.ts',
#        outroFrames
#    )

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
        if event['room'] not in ('Keynote Room BB007', 'ROOM2'):
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

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile = 'background.svg',
            outfile = 'background.ts',
            sequence = backgroundFrames
        ))
