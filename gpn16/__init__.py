#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://entropia.de/GPN16:Fahrplan:XML?action=raw'

# For (really) too long titles
titlemap = {
}

def bounce(i, min, max, frames):
    if i == frames - 1:
        return 0

    if i <= frames/2:
        return easeInOutQuad(i, min, max, frames/2)
    else:
        return max - easeInOutQuad(i - frames/2, min, max, frames/2)

def introFrames(parameters):
        frames = 10
        for i in range(0, frames):
                yield (
                        ('eatTransform',         'attr',  'transform', "scale(%.4f)" % easeLinear(i, 0.5, 2.0, frames)),
                        ('eatTransform',        'style', 'opacity',  '%.4f' % bounce(i, 0.0, 1.0, frames))
                )

        frames = 10
        for i in range(0, frames):
                yield (
                        ('sleep',         'attr',  'transform', "scale(%.4f)" % easeLinear(i, 0.5, 2.0, frames)),
                        ('sleepTransform',        'style', 'opacity',  '%.4f' % bounce(i, 0.0, 1.0, frames))
                )

        frames = 10
        for i in range(0, frames):
                yield (
                        ('codeTransform',         'attr',  'transform', "scale(%.4f)" % easeLinear(i, 0.5, 2.0, frames)),
                        ('codeTransform',        'style', 'opacity',  '%.4f' % bounce(i, 0.0, 1.0, frames))
                )

        frames = 10
        for i in range(0, frames):
                yield (
                        ('repeatTransform',         'attr',  'transform', "scale(%.4f)" % easeLinear(i, 0.5, 2.0, frames)),
                        ('repeatTransform',        'style', 'opacity',  '%.4f' % bounce(i, 0.0, 1.0, frames))
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
    frames = 5*fps
    for i in range(0, frames):
        percentage = easeLinear(i, 0, 10, frames)
        yield (
                ('glow',   'attr',     'x', '%.4f' %  (-0.045 * percentage / 10 )),
                ('glow',   'attr',     'y', '%.4f' %  (-0.09 * percentage / 10 )),
                ('glow',   'attr',     'width', '%.4f' % (1 + percentage / 10 * 0.18) ),
                ('glow',   'attr',     'height', '%.4f' % (1 + percentage / 10 * 0.36) ),
                ('glowBlur',   'attr',     'stdDeviation', '%.4f' % (percentage / 10 * 19.858825)),
                )

def debug():
	render(
	'intro.svg',
	'../intro.ts',
        introFrames
        )
	# render(
	# 	'outro.svg',
	# 	'../outro.ts',
	# 	outroFrames
	# )
	#render(
	#	'intro.svg',
	#	'../intro.ts',
	#	introFrames,
	#	{
	#		'$id': 20227,
	#		'$title': "Leben mit dem Saurier",
	#		'$subtitle': '',
	#		'$personnames': 'Sarah'
	#	}
	#)

def tasks(queue, parameters):
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
                    '$id': event['id'],
                    '$title': event['title'],
                    '$subtitle': event['subtitle'],
                    '$personnames': event['personnames']
                    }
                ))
