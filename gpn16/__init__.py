#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://entropia.de/GPN16:Fahrplan:XML?action=raw'

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
        yield (
            ('textblock',   'style', 'opacity',  '%.4f' % 0),
            ('layer-icons', 'style', 'display',  'inline'),

            ('eat',         'style', 'opacity',  '%.4f' % 0),
            ('sleep',       'style', 'opacity',  '%.4f' % 0),
            ('code',        'style', 'opacity',  '%.4f' % 0),
            ('repeat',      'style', 'opacity',  '%.4f' % 0),
        )

        for icon in ('eat', 'sleep', 'code', 'repeat'):
            frames = 12
            for i in range(0, frames):
                scale = easeLinear(i, 0.5, 2, frames)
                move = -0.5 * scale + 0.5
                x = 1920 * move
                y = 1080 * move
                yield (
                    (icon,         'attr',  'transform', "translate(%.4f, %.4f) scale(%.4f)" % (x, y, scale)),
                    (icon,         'style', 'opacity',  '%.4f' % bounce(i, 0.0, 1.0, frames))
                )

        frames = 12
        for i in range(0, frames):
                scale = easeLinear(i, 0.5, 0.5, frames)
                move = -0.5 * scale + 0.5
                x = 1920 * move
                y = 1080 * move
                yield (
                        ('textblock',   'attr',  'transform', "translate(%.4f, %.4f) scale(%.4f)" % (x, y, scale)),
                        ('textblock',   'style', 'opacity',  '%.4f' % easeLinear(i, 0.0, 1.0, frames))
                )

        frames = 25*3
        for i in range(0, frames):
            yield (
                    ('textblock',   'attr',  'transform', "scale(%.4f)" % 1),
                    ('textblock',   'style', 'opacity',  '%.4f' % 1)
            )

        frames = 12
        for i in range(0, frames):
                scale = easeLinear(i, 1, 1.5, frames)
                move = -0.5 * scale + 0.5
                x = 1920 * move
                y = 1080 * move
                yield (
                        ('textblock',   'attr',  'transform', "translate(%.4f, %.4f) scale(%.4f)" % (x, y, scale)),
                        ('textblock',   'style', 'opacity',  '%.4f' % easeLinear(i, 1.0, -1.0, frames))
                )

        frames = 5
        for i in range(0, frames):
            yield (
                    ('textblock',   'style', 'opacity',  '%.4f' % 0),
            )

# def outroFrames(parameters):
#     frames = 2*fps
#     for i in range(0, frames):
#         yield (
#                 ('license',       'style', 'opacity', "0.0"),
#                 ('gpn',           'style', 'opacity', "1.0"),
#             )

#     frames = 2*fps
#     for i in range(0, frames):
#         yield (
#                 ('gpn',           'style', 'opacity', "%.4f" % easeOutCubic(min(i,frames/2), 1, -1, frames/2)),
#                 ('license',       'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
#             )

#     frames = 1*fps
#     for i in range(0, frames):
#         yield (
#                 ('license',       'style', 'opacity', "1.0"),
#                 ('gpn',           'style', 'opacity', "0.0"),
#             )

def pauseFrames(parameters):
        yield (
            ('layer-icons', 'style', 'display',  'inline'),

            ('eat',         'style', 'opacity',  '%.4f' % 0),
            ('sleep',       'style', 'opacity',  '%.4f' % 0),
            ('code',        'style', 'opacity',  '%.4f' % 0),
            ('repeat',      'style', 'opacity',  '%.4f' % 0),
        )

        for icon in ('eat', 'sleep', 'code', 'repeat'):
            frames = 12
            for i in range(0, frames):
                yield (
                    ('eat',         'style', 'opacity',  '%.4f' % 0),
                    ('sleep',       'style', 'opacity',  '%.4f' % 0),
                    ('code',        'style', 'opacity',  '%.4f' % 0),
                    ('repeat',      'style', 'opacity',  '%.4f' % 0),

                    (icon,          'style', 'opacity',  '%.4f' % bounce(i, 0.0, 1.0, frames)),
                )


def outroFrames(p):
    # 5 Sekunden stehen bleiben
    frames = 5*fps
    for i in range(0, frames):
        yield []

def debug():
    render(
        'intro.svg',
        '../intro.ts',
        introFrames
    )

    render(
        'pause.svg',
        '../pause.ts',
        pauseFrames
    )

    render(
      'outro.svg',
      '../outro.ts',
      outroFrames
    )

    #render(
    #   'intro.svg',
    #   '../intro.ts',
    #   introFrames,
    #   {
    #       '$id': 20227,
    #       '$title': "Leben mit dem Saurier",
    #       '$subtitle': '',
    #       '$personnames': 'Sarah'
    #   }
    #)

def tasks(queue, args):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):

        if len(args) > 0:
            if not str(event['id']) in args:
                continue

        # generate a task description and put it into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$ID': event['id'],
                '$TITLE': event['title'],
                '$SUBTITLE': event['subtitle'],
                '$SPEAKER': event['personnames']
                }
            ))
