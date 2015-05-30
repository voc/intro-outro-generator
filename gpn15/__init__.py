#!/usr/bin/python

import subprocess
import os.path
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'http://bl0rg.net/~andi/gpn15-fahrplan/schedule.xml'

# For (really) too long titles
titlemap = {
}

def introFrames(parameters):
        # 5 Sekunden

        # 1 Sekunden stehen bleiben
        frames = 1*fps
        for i in range(0, frames):
                yield (
                        ('rain',           'style', 'opacity', "1.0"),
                        ('personnames',   'style', 'opacity', "0.0"),
                        ('title',         'style', 'opacity', "0.0"),
                )

        # 3 Sekunden Fade-in
        frames = 3*fps
        for i in range(0, frames):
                yield (
                        ('rain',           'style', 'opacity', "%.4f" % easeOutCubic(min(i,frames/2), 1, -1, frames/2)),
                        ('personnames',   'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                        ('title',         'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                )

        # 1 Sekunden stehen bleiben
        frames = 1*fps
        for i in range(0, frames):
                yield (
                )


def outroFrames(parameters):
    frames = 2*fps
    for i in range(0, frames):
        yield (
                ('license',       'style', 'opacity', "0.0"),
                ('gpn',           'style', 'opacity', "1.0"),
            )

    frames = 2*fps
    for i in range(0, frames):
        yield (
                ('gpn',           'style', 'opacity', "%.4f" % easeOutCubic(min(i,frames/2), 1, -1, frames/2)),
                ('license',       'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
            )

    frames = 1*fps
    for i in range(0, frames):
        yield (
                ('license',       'style', 'opacity', "1.0"),
                ('gpn',           'style', 'opacity', "0.0"),
            )

def pauseFrames(parameters):
    frames = 5*fps
    for i in range(0, frames):
        yield (
                ('rain',   'attr',     'transform', 'translate(0,%.4f)' % easeLinear(i, 0, 448, frames) ),
                )

    frames = 5*fps
    for i in range(0, frames):
        yield (
                ('rain',   'attr',     'transform', 'translate(0,%.4f)' % easeLinear(i, 0, 448, frames) ),
                )

    frames = 5*fps
    for i in range(0, frames):
        yield (
                ('rain',   'attr',     'transform', 'translate(0,%.4f)' % easeLinear(i, 0, 448, frames) ),
                )

def debug():
	#render(
	#	'pause.svg',
	#	'../pause.ts',
	#	pauseFrames
	#)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

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
