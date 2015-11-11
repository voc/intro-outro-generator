#!/usr/bin/python3

from renderlib import *
from easing import *
import math

# URL to Schedule-XML
scheduleUrl = 'https://n621.de/fud/nixcon.xml'

# For (really) too long titles
titlemap = {
    #708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}

def introFrames(params):
    move=40

    # wait
    frames = 1*fps
    for i in range(0, frames):
        yield (
        )

    deltas = {}
    for segment in range(1, 7):
        angle = 60 * (segment - 1)
        dist = 1000

        dx = -dist * math.cos(math.radians(angle))
        dy = -dist * math.sin(math.radians(angle))

        deltas[segment] = (dx, dy)

    # fly out
    frames = int(1.5*fps)
    for i in range(0, frames):
        placements = []
        for segment in range(1, 7):
            x = easeInCubic(i, 0, deltas[segment][0], frames)
            y = easeInCubic(i, 0, deltas[segment][1], frames)
            opacity = 1 - easeInCubic(i, 0, 1, int(0.8*frames))

            placements.extend([
                ('segment%u' % segment, 'attr', 'transform', 'translate(%.4f, %.4f)' % (x, y)),
                ('segment%u' % segment, 'style', 'opacity', '%.4f' % opacity)
            ])

        logotext_dx = easeInCubic(i, 0, 2000, frames)
        logotext_opacity = 1 - easeInCubic(i, 0, 1, 20)

        placements.extend([
            ('logotext', 'attr', 'transform', 'translate(%.4f, 0)' % logotext_dx),
            ('logotext', 'style', 'opacity', '%.4f' % logotext_opacity),
        ])

        if i > int(frames/2):
            sub_frames = frames - int(frames/2)
            sub_i = i - int(frames/2)

            talk_opacity = easeInCubic(sub_i, 0, 1, sub_frames)

            placements.extend([
                ('title', 'style', 'opacity', '%.4f' % talk_opacity),
                ('person', 'style', 'opacity', '%.4f' % talk_opacity),
            ])


        yield placements

    # wait
    frames = int(2.5*fps)
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', '%.4f' % 1),
            ('person', 'style', 'opacity', '%.4f' % 1),
        )

def outroFrames(params):
    pass


def debug():
    #render(
    #    'outro.svg',
    #    '../outro.dv',
    #    outroFrames
    #)

    render(
        'intro.svg',
        '../intro.dv',
        introFrames,
        {
            '$id': 904,
            '$title': 'The sorry state of Python packaging and how it reflects in Nix',
            '$personnames': 'Domen Kožar'
        }
    )

def tasks(queue, params):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl, titlemap):

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".dv",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$personnames': event['personnames']
            }
        ))

        # place a task for the outro into the queue
        #queue.put(Rendertask(
        #        infile = 'outro.svg',
        #        outfile = 'outro.dv',
        #        sequence = outroFrames
        #))
