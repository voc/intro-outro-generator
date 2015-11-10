#!/usr/bin/python

import subprocess
import os.path
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'https://frab.sendegate.de/de/ppw15b/public/schedule.xml'

# For (really) too long titles
titlemap = {
}

def easeOutCubic(t, b, c, d):
    t=float(t)/d-1
    return c*((t)*t*t + 1) + b

def introFrames(parameters):
        # 8 Sekunden

        # 1 Sekunden stehen bleiben
        frames = 1*fps
        for i in range(0, frames):
                yield (
                        ('flowRoot3405', 'style', 'opacity', "0.0"),
                        ('logo', 'style', 'opacity', "1"),
                )

        # 2 Sekunden Fade-in
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('logo', 'style', 'opacity', "1"),
                        ('flowRoot3405', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                )

        # 5 Sekunden stehen bleiben
        frames = 8*fps
        for i in range(0, frames):
                yield (
                )

def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$title': "Podcasten aus dem Bundestag – die Entstehung eines politischen Formats",
			'$subtitle': 'Alles über Technische Aufklärung',
			'$personnames': 'Felix Betzin, Jonas Schönfelder'
		}
	)

def tasks(queue, parameters):
    # iterate over all events extracted from the schedule xml-export
        for event in events(scheduleUrl):
            # generate a task description and put it into the queue
            queue.put(Rendertask(
                infile = 'intro.svg',
                outfile = str(event['id'])+".ts",
                sequence = introFrames,
                parameters = {
                    '$title': event['title'],
                    '$subtitle': event['subtitle'],
                    '$personnames': event['personnames']
                    }
                ))
