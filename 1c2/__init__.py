#!/usr/bin/python3

from renderlib import *
from itertools import zip_longest

# URL to Schedule-XML
scheduleUrl = 'http://chaos.cologne/Fahrplan/schedule.xml'

# For (really) too long titles
titlemap = {

}

def introFramesLight(p):
    frames = int(1.5*fps)
    max_opac = 0.7

    while True:
        for i in range(0, frames):
            yield [
                ('one', 'style', 'stroke-opacity', '{:.4f}'.format(easeLinear(i, 0, max_opac, frames)))
            ]
        for i in range(0, frames):
            yield [
                ('one', 'style', 'stroke-opacity', '{:.4f}'.format(easeLinear(frames-i, 0, max_opac, frames))),
                ('cee', 'style', 'stroke-opacity', '{:.4f}'.format(easeLinear(i, 0, max_opac, frames)))
            ]
        for i in range(0, frames):
            yield [
                ('cee', 'style', 'stroke-opacity', '{:.4f}'.format(easeLinear(frames-i, 0, max_opac, frames))),
                ('two', 'style', 'stroke-opacity', '{:.4f}'.format(easeLinear(i, 0, max_opac, frames)))
            ]
        for i in range(0, frames):
            yield [
                ('two', 'style', 'stroke-opacity', '{:.4f}'.format(easeLinear(frames-i, 0, max_opac, frames)))
            ]

def introFramesDot(p):
    frames = int(9.5 * fps)
    steps  = [
        (0, 0),
        (0, 159),
        (-848, 159),
        (-848, 53),
        (-742, 53),
        (-742, -106),
        (-795, -106),
        (-795, -212),
        (-742, -212),
        (-742, -265),
        (-583, -265),
        (-583, -212),
        (-424, -212),
        (-424, -265),
        (-106, -265),
        (-106, -212),
        (0, -212),
        (0, -53),
        (0, 0)
    ]

    steps_with_shift = [(0,0,0)]
    total_shift = 0
    for (oldx, oldy), (x, y) in zip(steps, steps[1:]):
        duration = abs(x - oldx) + abs(y - oldy)
        total_shift += duration
        steps_with_shift.append((duration, x, y))

    prev = (0, 0, 0)
    for step in steps_with_shift:
        dur = int(frames * step[0] / total_shift)
        for i in range(0, dur):
            yield [
                ('dot1', 'attr', 'transform', 'translate({:.4f}, {:.4f})'.format(easeLinear(i, prev[1], step[1]-prev[1], dur),
                                                                                 easeLinear(i, prev[2], step[2]-prev[2], dur)))
            ]
        prev = step

    for _ in range(int(0.5 * fps)):
        yield [
            ('dot1', 'attr', 'transform', 'translate(0, 0)')
        ]

def introFrameText(p):
    frames = 2*fps

    for i in range(0, frames):
        yield [
            ('text', 'style', 'opacity', '{:.4f}'.format(easeLinear(i, 0, 1, frames)))
        ]

def introFrames(p):
    for (i, j), z in zip_longest(zip(introFramesDot(p), introFramesLight(p)), introFrameText(p), fillvalue=[]):
        yield i + j + z

def outroFrames(p):
    # 5 Sekunden stehen bleiben
    frames = 5*fps
    for i in range(0, frames):
        yield []

def debug():
    render(
        'intro.svg',
        '../intro.ts',
        introFrames,
        parameters={
            '$id': 4711,
            '$title': 'D\'r Dom',
            '$subtitle': 'Hauptbahnhof',
            '$personnames': 'Tünnes und Schäl'
        }
    )

    render(
        'outro.svg',
        '../outro.ts',
        outroFrames
    )

def tasks(queue, args):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+'.ts',
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
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
