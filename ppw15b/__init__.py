#!/usr/bin/python
import subprocess
import os.path
from renderlib import *

# URL to Schedule-XML
scheduleUrl = 'https://frab.sendegate.de/de/ppw15b/public/schedule.xml'

def easeOutCubic(t, b, c, d):
    t=float(t)/d-1
    return c*((t)*t*t + 1) + b

def introFrames(parameters):
    # 1 Sekunden stehen bleiben
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', "1"),
            ('flowRoot3405', 'style', 'opacity', "0.0")
        )

    # 2 Sekunden Fade-in
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', "1"),
            ('flowRoot3405', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
        )

    # 5 Sekunden stehen bleiben
    frames = 5*fps
    for i in range(0, frames):
        yield ()

def outroFrames(parameters):
    frames = 5*fps
    for i in range(0, frames):
        yield ()

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

    render(
        'outro.svg',
        '../outro.ts',
        outroFrames
    )

def tasks(queue, parameters):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        # HACK: only render event 49
        #if event['id'] != 49:
        #   continue

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

    queue.put(Rendertask(
        infile = 'outro.svg',
        outfile = 'outro.ts',
        sequence = outroFrames
    ))
