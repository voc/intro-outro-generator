#!/usr/bin/python3

from renderlib import *
from easing import *

import math

# URL to Schedule-XML
scheduleUrl = 'https://talks.mrmcd.net/2023/schedule.xml'

speedfactor=1
def introFrames(args):
# sleep .5s
    frames = round(.5*fps*speedfactor)
    for i in range(0, frames*2):
        yield (
            ('houses', 'style', 'opacity', 0),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 0),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# fade in houses and sleep one second
    frames = round(1*fps*speedfactor)
    for i in range(0, frames*2):
        yield (
            ('houses', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 0),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# move in person
    frames = round(1*fps*speedfactor)
    for i in range(0, frames):
        t=i/frames
        pos=420*(1-t)
        print('i {}, t {}, pos {}'.format(i, t, pos))
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 1),
            ('person', 'attr', 'transform', 'translate(0.0, {})'.format(pos)),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )

# sleep 1s
    for i in range(0, round(1*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# look around
    for i in range(0, round(.5*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 1),
            ('person', 'attr', 'transform', 'matrix(-1,0,0,1,1420.2663,0)'),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
    for i in range(0, round(.5*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# sleep 1s
    for i in range(0, round(1*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# bonk once
    for i in range(0, math.ceil(.1*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 0),
            ('personhit', 'style', 'opacity', 1),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# wait 1s
    for i in range(0, 1*fps*speedfactor):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# bonk twice
    for j in range(0,2):
        for i in range(0, math.ceil(.1*fps*speedfactor)):
            yield (
                ('houses', 'style', 'opacity', 1),
                ('vr', 'style', 'opacity', 1),
                ('person', 'style', 'opacity', 0),
                ('personhit', 'style', 'opacity', 1),
                ('motto', 'style', 'opacity', 0),
                ('logotext', 'style', 'opacity', 0),
                ('text', 'style', 'opacity',  0),
                ('title', 'style', 'opacity', 0),
                ('subtitle', 'style', 'opacity', 0),
                ('persons', 'style', 'opacity', 0),
                ('id', 'style', 'opacity', 0),
            )
#        for i in range(0, round(.1*fps*speedfactor)):
#            yield (
#                ('houses', 'style', 'opacity', 1),
#                ('vr', 'style', 'opacity', 0),
#                ('vr-blurry', 'style', 'opacity', j),
#                ('person', 'style', 'opacity', 0),
#                ('personhit', 'style', 'opacity', 1),
#                ('motto', 'style', 'opacity', 0),
#                ('logotext', 'style', 'opacity', 0),
#                ('text', 'style', 'opacity',  0),
#                ('title', 'style', 'opacity', 0),
#                ('subtitle', 'style', 'opacity', 0),
#                ('persons', 'style', 'opacity', 0),
#                ('id', 'style', 'opacity', 0),
#            )
        for i in range(0, round(.2*fps*speedfactor)):
            yield (
                ('houses', 'style', 'opacity', 1),
                ('vr', 'style', 'opacity', 0),
                ('vr-blurry', 'style', 'opacity', j),
                ('person', 'style', 'opacity', 1),
                ('personhit', 'style', 'opacity', 0),
                ('motto', 'style', 'opacity', 0),
                ('logotext', 'style', 'opacity', 0),
                ('text', 'style', 'opacity',  0),
                ('title', 'style', 'opacity', 0),
                ('subtitle', 'style', 'opacity', 0),
                ('persons', 'style', 'opacity', 0),
                ('id', 'style', 'opacity', 0),
            )
# wait 1s
    for i in range(0, round(1*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('vr-blurry', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# bonk for speaker
    for i in range(0, round(.1*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 0),
            ('person', 'style', 'opacity', 0),
            ('personhit', 'style', 'opacity', 1),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# wait 1s
    for i in range(0, round(1*fps*speedfactor)):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity', 0),
            ('motto', 'style', 'opacity', 0),
            ('logotext', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  0),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# fade in speaker
    frames =  round(1*fps*speedfactor)
    for i in range(0, frames):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity',0),
            ('motto', 'style', 'opacity', 0),
            ('text', 'style', 'opacity',  easeInQuad(i, 0, 1, frames)),
            ('vr-darkening', 'style', 'opacity',  easeInQuad(i, 0, .4, frames)),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# fade in wgdh
    frames =  round(1*fps*speedfactor)
    for i in range(0, frames):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity',0),
            ('motto', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('text', 'style', 'opacity',  1),
            ('vr-darkening', 'style', 'opacity',  .4),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
# sleep 
    frames =  round(6*fps*speedfactor)
    for i in range(0, frames):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity',0),
            ('motto', 'style', 'opacity', 1),
            ('text', 'style', 'opacity',  1),
            ('vr-darkening', 'style', 'opacity',  .4),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )

def introShort(parameters):
    frames =  round(3*fps*speedfactor)
    for i in range(0, frames):
        yield (
            ('houses', 'style', 'opacity', 1),
            ('vr', 'style', 'opacity', 1),
            ('person', 'style', 'opacity', 1),
            ('personhit', 'style', 'opacity',0),
            ('motto', 'style', 'opacity', 1),
            ('text', 'style', 'opacity',  1),
            ('vr-darkening', 'style', 'opacity',  .4),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('persons', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
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
    frames = 6*fps
    for i in range(0, frames):
        yield(
        )

def pauseFrames(args):
#typing
    for j in range(0,8):
        typespeed = .2
        for i in range(0, round(typespeed*fps)):
            yield(
                ('person-default', 'style', 'opacity', 1),
                ('person-key', 'style', 'opacity', 0),
                ('person-frown', 'style', 'opacity', 0),
                ('person-vr', 'style', 'opacity', 0),
            )
        for i in range(0, round(typespeed*fps)):
            yield(
                ('person-default', 'style', 'opacity', 0),
                ('person-key', 'style', 'opacity', 1),
                ('person-frown', 'style', 'opacity', 0),
                ('person-vr', 'style', 'opacity', 0),
            )
#sleep
    for i in range(0, round(1*fps)):
        yield(
            ('person-default', 'style', 'opacity', 1),
            ('person-key', 'style', 'opacity', 0),
            ('person-frown', 'style', 'opacity', 0),
            ('person-vr', 'style', 'opacity', 0),
            ('graffiti', 'style', 'opacity', 0),
        )
#frown
    for i in range(0, round(1*fps)):
        yield(
            ('person-default', 'style', 'opacity', 0),
            ('person-key', 'style', 'opacity', 0),
            ('person-frown', 'style', 'opacity', 1),
            ('person-vr', 'style', 'opacity', 0),
            ('graffiti', 'style', 'opacity', 0),
        )
#bonk headset
    for j in range(0,3):
        bonkspeed = .2
        for i in range(0, round(bonkspeed*fps)):
            yield(
                ('person-default', 'style', 'opacity', 0),
                ('person-key', 'style', 'opacity', 0),
                ('person-frown', 'style', 'opacity', 1),
                ('person-vr', 'style', 'opacity', 0),
                ('graffiti', 'style', 'opacity', 0),
            )
        for i in range(0, round(bonkspeed*fps)):
            yield(
                ('person-default', 'style', 'opacity', 0),
                ('person-key', 'style', 'opacity', 0),
                ('person-frown', 'style', 'opacity', 0),
                ('person-vr', 'style', 'opacity', 1),
                ('graffiti', 'style', 'opacity', 0),
            )
#frown
    for i in range(0, round(1*fps)):
        yield(
            ('person-default', 'style', 'opacity', 0),
            ('person-key', 'style', 'opacity', 0),
            ('person-frown', 'style', 'opacity', 1),
            ('person-vr', 'style', 'opacity', 0),
            ('graffiti', 'style', 'opacity', 1),
        )
#smile
    for i in range(0, round(1*fps)):
        yield(
            ('person-default', 'style', 'opacity', 1),
            ('person-key', 'style', 'opacity', 0),
            ('person-frown', 'style', 'opacity', 0),
            ('person-vr', 'style', 'opacity', 0),
            ('graffiti', 'style', 'opacity', 1),
        )


def debug():
#    render('intro.svg',
#        '../intro.ts',
#        introFrames,
#        {
#            '$id': 7776,
#            '$title': 'Memetische Agitation des jungen Rechtsau&#223;enspektrums: Mechanismen, Strategien, Narrative',
#            '$subtitle': '',
#            '$persons':  'Vincent Knopp'
#        }
#    )
    
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'Memetische Agitation des jungen Rechtsaußenspektrums: Mechanismen, Strategien, Narrative',
            '$subtitle': '',
            '$persons':  'Berlin Busters Social Club'
        }
    )

#    render('outro.svg',
#        '../outro.ts',
#        outroFrames
#    )
#
#    render(
#        'background.svg',
#        '../background.ts',
#        backgroundFrames
#    )
#
#    render('pause.svg',
#        '../pause.ts',
#        pauseFrames
#    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
#        if event['room'] not in ('Chirurgie (Saal 1.04)', 'Kreißsaal (Saal 1.11)'):
#            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
#            continue
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
