#!/usr/bin/python3

from renderlib import *
from easing import *
from math import sin, pi

scheduleUrl = 'https://babelmonkeys.de/~florob/sj19-schedule.xml'

def introFrames(p):

    handle1_off = 120
    handle2_off = 247
    handle3_off = 80

    # kurz stehen bleiben
    frames = int(0.5 * fps)
    for i in range(0, frames):
        yield (
            ('handle1', 'attr', 'transform', "translate(0, {})".format(handle1_off)),
            ('handle2', 'attr', 'transform', "translate(0, {})".format(handle2_off)),
            ('handle3', 'attr', 'transform', "translate(0, {})".format(handle3_off)),
        )

    # handle 1 anheben
    frames = 3 * fps
    for i in range(0, frames):
        y = (1.0 - i / frames) * handle1_off
        yield (
            ('handle1', 'attr', 'transform', "translate(0, {})".format(y)),
            ('handle2', 'attr', 'transform', "translate(0, {})".format(handle2_off)),
            ('handle3', 'attr', 'transform', "translate(0, {})".format(handle3_off)),
        )

    # kurz stehen bleiben
    frames = int(0.2 * fps)
    for i in range(0, frames):
        yield (
            ('handle2', 'attr', 'transform', "translate(0, {})".format(handle2_off)),
            ('handle3', 'attr', 'transform', "translate(0, {})".format(handle3_off)),
        )

    # handle 2 anheben
    frames = 3 * fps
    for i in range(0, frames):
        y = (1.0 - i / frames) * handle2_off
        yield (
            ('handle2', 'attr', 'transform', "translate(0, {})".format(y)),
            ('handle3', 'attr', 'transform', "translate(0, {})".format(handle3_off)),
        )

    # kurz stehen bleiben
    frames = int(0.2 * fps)
    for i in range(0, frames):
        yield (
            ('handle3', 'attr', 'transform', "translate(0, {})".format(handle3_off)),
        )

    # handle 3 anheben
    frames = 3 * fps
    for i in range(0, frames):
        y = (1.0 - i / frames) * handle3_off
        yield (
            ('handle3', 'attr', 'transform', "translate(0, {})".format(y)),
        )

    # kurz stehen bleiben
    frames = int(0.5 * fps)
    for i in range(0, frames):
        yield ()

def pauseFrames(p):
    handle1_off = 110
    handle2_off = 150
    handle3_off = 110

    frames = 10 * fps
    for i in range(0, frames):
        yield (
            ('handle1', 'attr', 'transform', "translate(0, {})".format(sin(2 * pi * i / frames) * handle1_off)),
            ('handle2', 'attr', 'transform', "translate(0, {})".format(sin(2 * pi * i / frames + 0.5 * pi) * handle2_off)),
            ('handle3', 'attr', 'transform', "translate(0, {})".format(sin(2 * pi * i / frames + 1.0 * pi) * handle3_off)),
        )

def outroFrames(p):
    # 5 Sekunde stehen lassen
    frames = 5 * fps
    for i in range(0, frames):
        yield ()


def debug():
    render(
        'intro.svg',
        '../18271.ts',
        introFrames,
        {
            '$date': "October 27th, 2018",
            '$title': "Welcome",
            '$subtitle': 'What is Open Source?',
            '$personnames': 'Nils Hilbricht'
        }
    )

    render(
        'outro.svg',
        '../outro.ts',
        outroFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if not (idlist == []):
            if 000000 in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue
            if int(event['id']) not in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile='intro.svg',
            outfile=str(event['id']) + ".ts",
            sequence=introFrames,
            parameters={
                '$date': "October 4th, 2017",
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'] or '',
                '$personnames': event['personnames']
            }
        ))

    if not "pause" in skiplist:
        queue.put(Rendertask(
            infile='pause.svg',
            outfile='pause.ts',
            sequence=pauseFrames
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile='outro.svg',
            outfile='outro.ts',
            sequence=outroFrames
        ))
