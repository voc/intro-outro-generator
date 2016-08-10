#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://static.gnome.org/guadec-2016/schedule.xml'

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
    firstmove=2100
    move=100


    # 0.5 seconds blue
    frames = int(fps/2)
    for i in range(0, frames):
        yield (
            ('fadetoblack', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames-1)),
            ('title', 'style',    'opacity', "0"),
            ('longtitle', 'style',    'opacity', "0"),
            ('presentedby', 'style',    'opacity', "0"),
            ('speaker', 'style',    'opacity', "0"),
            ('longspeaker', 'style',    'opacity', "0"),
            ('overlay', 'style',    'opacity', "0"),
            ('guadeclogo', 'style',    'opacity', "0"),
            ('onlinediscussion', 'style',    'opacity', "0"),
        )

    # 0.5 seconds background fade in
    frames = int(fps/2)
    for i in range(0, frames):
        yield (
            ('guadeclogo', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('overlay', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('overlay', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, firstmove, -firstmove, frames-1)),
        )

    # 0.6 seconds still
    frames = int(fps/1.75)
    for i in range(0, frames):
        yield ()

    # 0.2 seconds title text fade in
    frames = int(fps/5)
    for i in range(0, frames):
        yield (
            ('title', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('longtitle', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('titletranslator', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
        )

    # 0.2 seconds presented by text fade in
    frames = int(fps/5)
    for i in range(0, frames):
        yield (
            ('presentedby', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('presentedby', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
        )
    # 0.2 seconds speaker text fade in
    frames = int(fps/5)
    for i in range(0, frames):
        yield (
            ('speaker', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('longspeaker', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('speakertranslator', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
            ('onlinediscussion', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
        )

    # 4 seconds still
    frames = 4*fps
    for i in range(0, frames):
        yield (
            ('title', 'style',    'opacity', "1"),
            ('longtitle', 'style',    'opacity', "1"),
            ('presentedby', 'style',    'opacity', "1"),
            ('speaker', 'style',    'opacity', "1"),
            ('longspeaker', 'style',    'opacity', "1"),
        )

def pauseFrames(p):
    # pulsing on hold with 1,5 seconds interval
    frames = int(1.3*fps)
    for i in range(0, frames):
        yield (
            ('onhold', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -0.8, frames-1)),
        )
        
    frames = int(1.5*fps)
    for i in range(0, frames):
        yield (
            ('onhold', 'style',    'opacity', "%.4f" % easeLinear(i, 0.2, 1, frames-1)),
        )



def outroFrames(p):
    # 7 seconds of slow scaling, fade to black at the end
    frames = 7*fps
    for i in range(0, frames):
        scale = easeLinear(i, 1.3, 0.3  , frames-1)
        opacity = 0
        if i > int(frames*0.7):
            opacity = easeLinear(int(i-frames*0.7), 0, 1, int(frames-frames*0.7)-1)      
        yield (
            ('guadeclogoscale', 'attr', 'transform', 'scale({scale},{scale})'.format(scale=scale),),
            ('fadetoblack', 'style',    'opacity', '{opac}'.format(opac=opacity),),
        )

   # 2 seconds of black
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('fadetoblack', 'style',    'opacity', "1"),
        )

        
def debug():
    render(
      'intro.svg',
      '../intro.ts',
      introFrames,
      {
          '$title': "Long Long Long title is LONG",
          '$sub': 'Long Long Long Long subtitle is LONGER',
          '$speaker': 'Long Name of Dr. Dr. Prof. Dr. Long Long'
      }
    )

    render(
        'pause.svg',
        '../pause.ts',
        pauseFrames,
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

        if len(event['title']) < 71: 
            params = {
                '$title': event['title'],
                '$longtitle': '',
                '$speaker': '',
                '$longspeaker': event['personnames']
                }
        else:
            params = {
                '$title': '',
                '$longtitle': event['title'],
                '$speaker': '',
                '$longspeaker': event['personnames']
                }

        # generate a task description and put it into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = params
            ))
