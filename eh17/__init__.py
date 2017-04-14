#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from easing import *
import svg.path
import random
from itertools import permutations


# URL to Schedule-XML
scheduleUrl = 'https://eh17.easterhegg.eu/Fahrplan/schedule.xml'

# For (really) too long titles
titlemap = {
    #
}


class animate(object):

    def __init__(self, low, high, xml):
        self.low = low * fps
        self.high = high * fps
        self.frames = self.high - self.low
        self.xml = xml

    def get(self, frame):

        if self.low <= frame <= self.high:
            return self.frame(frame)

    def relframe(self, frame):
        return frame - self.low


class background(animate):

    def __init__(self, low, high, xml):
        animate.__init__(self, low, high, xml)

        self.pathstr = xml.find(".//*[@id='animatePath']").get('d')
        self.path = svg.path.parse_path(self.pathstr)
        self.init = self.path.point(0)

    def frame(self, frame):
        p = self.path.point(self.relframe(frame) / self.frames) - self.init
        return (
           ('bgtext', 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),)


class logotext(animate):

    def __init__(self, low, high, xml):
        animate.__init__(self, low, high, xml)

        self.pathstr = xml.find(".//*[@id='textPath']").get('d')
        self.path = svg.path.parse_path(self.pathstr)
        self.init = self.path.point(0)

    def frame(self, frame):
        p = self.path.point(self.relframe(frame) / self.frames) - self.init
        return (
           ('ehtext', 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),)


class urldate(animate):

    def frame(self, frame):
        return(
            ('url', 'style', 'opacity', easeOutQuad(self.relframe(frame), 1, -1, self.frames)),
            ('date', 'style', 'opacity', easeOutQuad(self.relframe(frame), 0, 1, self.frames)),
            )


class hasenfarbe(animate):

    def __init__(self, low, high, xml):
        animate.__init__(self, low, high, xml)
        colors = ['#9e00a0', '#ffe72d', '#ff8600', '#0bc401', '#d40010', '#0049da']
        self.hasen = []
        for p in permutations(colors):
            self.hasen.append(p)
        random.shuffle(self.hasen)


    def frame(self, frame):
        if frame % 3 is 0:
            return(
                ('hase001', 'style', 'fill', self.hasen[frame][0]),
                ('hase002', 'style', 'fill', self.hasen[frame][0]),
                ('hase003', 'style', 'fill', self.hasen[frame][0]),
                ('hase004', 'style', 'fill', self.hasen[frame][0]),
                ('hase005', 'style', 'fill', self.hasen[frame][1]),
                ('hase006', 'style', 'fill', self.hasen[frame][1]),
                ('hase007', 'style', 'fill', self.hasen[frame][1]),
                ('hase008', 'style', 'fill', self.hasen[frame][2]),
                ('hase009', 'style', 'fill', self.hasen[frame][2]),
                ('hase010', 'style', 'fill', self.hasen[frame][2]),
                ('hase011', 'style', 'fill', self.hasen[frame][3]),
                ('hase012', 'style', 'fill', self.hasen[frame][3]),
                ('hase013', 'style', 'fill', self.hasen[frame][3]),
                ('hase014', 'style', 'fill', self.hasen[frame][4]),
                ('hase015', 'style', 'fill', self.hasen[frame][4]),
                ('hase016', 'style', 'fill', self.hasen[frame][4]),
                ('hase017', 'style', 'fill', self.hasen[frame][4]),
                ('hase018', 'style', 'fill', self.hasen[frame][5]),
                ('hase019', 'style', 'fill', self.hasen[frame][5]),
                ('hase020', 'style', 'fill', self.hasen[frame][5]),
                )


class cclogo(animate):

    def frame(self, frame):
        return (
            ('license', 'style', 'opacity', easeLinear(self.relframe(frame), 0, 1, self.frames)),
            )


def introFrames(args):
    xml = etree.parse('eh17/artwork/intro.svg').getroot()

    animations = [
        background(0, 6, xml),
        urldate(0.5, 1, xml),
        hasenfarbe(1, 5, xml),
        logotext(4, 5, xml)]

    frames = int(6 * fps)
    for frame in range(0, frames):

        frameactions = ()
        for a in animations:
                action = a.get(frame)
                if action:
                    frameactions += action

        print (frameactions)
        yield frameactions


def outroFrames(args):
    xml = etree.parse('eh17/artwork/outro.svg').getroot()

    animations = [
        background(0, 15, xml),
        hasenfarbe(1, 5, xml),
        cclogo(0.5, 2, xml)]

    frames = int(14 * fps)
    for frame in range(0, frames):

        frameactions = ()
        for a in animations:
                action = a.get(frame)
                if action:
                    frameactions += action

        print (frameactions)
        yield frameactions

def oldoutroFrames(args):
    xml = etree.parse('eh17/artwork/outro.svg').getroot()
    pathstr = xml.find(".//*[@id='animatePath']").get('d')
    frog = xml.find(".//*[@id='animatePath']").get('d')
    path = svg.path.parse_path(pathstr)

    init = path.point(0)

    frames = int(0.5 * fps)
    for i in range(0, frames):
        p = path.point(i / frames) - init
        yield (
            ('animatePath', 'style', 'opacity', 0),
            ('license', 'style', 'opacity', 0),
        )

    frames = 3 * fps
    for i in range(0, frames):
        p = path.point(i / frames) - init
        yield (
            ('frog', 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),
        )

    frames = int(0.5 * fps) + 1
    for i in range(0, frames):
        yield tuple()

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', 0),
            ('license', 'style', 'opacity', easeLinear(i, 0, 1, frames)),
        )

    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', 0),
            ('license', 'style', 'opacity', 1),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', 0),
            ('license', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', 0),
            ('license', 'style', 'opacity', 0),
        )

def pauseFrames(args):
    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('text1', 'style', 'opacity', 1),
            ('text2', 'style', 'opacity', 0),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('text1', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
            ('text2', 'style', 'opacity', 0),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('text1', 'style', 'opacity', 0),
            ('text2', 'style', 'opacity', easeLinear(i, 0, 1, frames)),
        )

    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('text1', 'style', 'opacity', 0),
            ('text2', 'style', 'opacity', 1),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('text1', 'style', 'opacity', 0),
            ('text2', 'style', 'opacity', easeLinear(i, 1, -1, frames)),
        )

    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('text1', 'style', 'opacity', easeLinear(i, 0, 1, frames)),
            ('text2', 'style', 'opacity', 0),
        )

def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 1302,
            '$title': 'VlizedLab - Eine Open Source-Virtualisierungslösung für PC-Räume',
            '$subtitle': 'IT Automatisierung und zentrales Management mit SALT',
            '$personnames': 'Thorsten Kramm',
            '$url':'blubb',
            '$date':'huhu'

        }
    )

# #    render('outro.svg',
#         '../outro.ts',
#         outroFrames
#     )
#
#     render('pause.svg',
#         '../pause.ts',
#         pauseFrames
#     )


def tasks(queue, args):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Vortragssaal', 'Großes Kolleg'):
            print("skipping room %s (%s)" % (event['room'], event['title']))
            continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile='intro.svg',
            outfile=str(event['id']) + ".ts",
            sequence=introFrames,
            parameters={
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$personnames': event['personnames']
            }
        ))

    # place a task for the outro into the queue
    queue.put(Rendertask(
        infile='outro.svg',
        outfile='outro.ts',
        sequence=outroFrames
    ))

    # place the pause-sequence into the queue
    queue.put(Rendertask(
        infile='pause.svg',
        outfile='pause.ts',
        sequence=pauseFrames
    ))
