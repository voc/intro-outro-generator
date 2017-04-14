#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from easing import *
import svg.path
from twisted.words.protocols.irc import lowDequote
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


class flyin(animate):

    def __init__(self, low, high, xml, svgid, runout=True):
        animate.__init__(self, low, high, xml)
        self.pathstr = xml.find(".//*[@id='flyinPath']").get('d')
        self.path = svg.path.parse_path(self.pathstr)
        self.init = self.path.point(0)
        self.stopf = self.relframe(self.high) / 3
        self.contf = 2 * self.stopf
        print(self.contf)
        self.svgid = svgid
        self.runout = runout

    def frame(self, frame):
        if self.relframe(frame) <= self.stopf:
            p = self.path.point(self.relframe(frame) / (self.frames)) - self.init
            self.stoppos = p
            return (
                (self.svgid, 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),)

        if self.runout and self.relframe(frame) >= self.contf:
            p = self.path.point(self.relframe(frame) / (self.frames)) - self.init - self.stoppos
            return (
                (self.svgid, 'attr', 'transform', 'translate(%.4f, %.4f)' % (p.real, p.imag)),)


def introFrames(args):
    xml = etree.parse('eh17/artwork/intro.svg').getroot()

    animations = [
        background(0, 15, xml),
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
        hasenfarbe(0, 15, xml),
        flyin(0.5, 2, xml, 'zufall'),
        flyin(1.5, 3, xml, 'ccby', False)]

    frames = int(4 * fps)
    for frame in range(0, frames):

        frameactions = ()
        for a in animations:
                action = a.get(frame)
                if action:
                    frameactions += action

        print (frameactions)
        yield frameactions


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
    render('outro.svg',
           '../outro.ts',
           outroFrames,
           {
            '$id': 1302,
            '$title': 'VlizedLab - Eine Open Source-Virtualisierungslösung für PC-Räume',
            '$subtitle': 'IT Automatisierung und zentrales Management mit SALT',
            '$personnames': 'Thorsten Kramm',
            '$url': 'blubb',
            '$date': 'huhu'
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
