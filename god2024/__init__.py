#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://import.c3voc.de/schedule/god2024.xml?showall=yes'

titlemap = {

}

def introFrames(p):
    givenFrame = 0

    nr = p['$id'];

    # 1 Sekunden nix
    frames = 1*fps
    for i in range(0, frames):
        givenFrame += 1
        yield (
            ('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
            ('layer1', 'style',    'opacity', "%.4f" % 0),  # nix
            # ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
        )

    # 1 Sekunde Text Fadein
    frames = 1*fps
    for i in range(0, frames):
        givenFrame += 1
        yield (
            ('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
            ('layer1', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
            # ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
        )

    # 5 Sekunden Text
    frames = 5*fps
    for i in range(0, frames):
        givenFrame += 1
        yield (
            ('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
            ('layer1', 'style',    'opacity', "%.4f" %1),
            # ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
        )

def outroFrames(p):
    xml = etree.parse('god2024/artwork/outro.svg').getroot()

    frames = int(5*fps)
    for i in range(0, frames):
        yield ()

def pauseFrames(p):
    # 1 sekunden fade in
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('text1', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
        )

    # 1 sekunde sehen
    for i in range(0, frames):
        yield (
            ('text1', 'style',    'opacity', "%.4f" % 1),
        )

    # 1 sekunde fadeout
    for i in range(0, frames):
        yield (
            ('text1', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
        )

    # 1 sekunde bild
    for i in range(0, frames):
        yield (
            ('text1', 'style',    'opacity', "%.4f" % 0),
        )

def debug():
    render(
        'intro.svg',
        '../intro.ts',
         introFrames,
        {
            '$id': 65,
            '$title': 'OWASP Juice Shop 10th anniversary: Is it still fresh?'.upper(),
            '$subtitle': '',
            '$personnames': 'Jannik Hollenbach'.upper(),
            #'only_render_frame': 353
            'only_rerender_frames_after': 225
        }
    )

    # render(
    #    'pause.svg',
    #    '../pause.ts',
    #    pauseFrames
    # )

def tasks(queue, args, id_list, skip_list):
    if not 'outro' in skip_list:
        # place a task for the outro into the queue
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
            ))

    if not 'pause' in skip_list:
        # place the pause-sequence into the queue
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
            ))

    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl, titlemap):

        # skip events which will not be recorded
        if event['room'] not in ('Da Capo',) or event['track'] == 'Nomnom':
            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            continue

        # when id_list is not empty, only render events which are in id_list
        if id_list and int(event['id']) not in id_list:
            print("skipping id (%s [%s])" % (event['title'], event['id']))
            continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id']) + ".ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'].upper(),
                '$subtitle': event['subtitle'],
                '$personnames': event['personnames'].upper(),
                }
            ))

