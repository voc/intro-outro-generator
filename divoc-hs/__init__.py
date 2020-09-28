#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://git.chaotikum.org/divoc/fahrplan/raw/master/fahrplan.xml'


def clamp(n, i, a):
    return max(min(n, a), i)


def introFrames(args):
    frames = int(.5*fps)
    for i in range(0, frames):
        yield (
            ('logo', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('personnames', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
    frames = int(.5*fps)
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', 0),
            ('personnames', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
    frames = int(1*fps)
    for i in range(0, frames):
        scale = easeInOutQuad(i, 1.0, -0.8, frames-1)
        dx = easeInOutQuad(i, 0, 1550, frames-1)
        dy = easeInOutQuad(i, 0, 875, frames-1)
        yield (
            ('logo', 'attr', 'transform', f'translate({dx}, {dy}) scale({scale},{scale})'),
            ('title', 'style', 'opacity', 0),
            ('subtitle', 'style', 'opacity', 0),
            ('personnames', 'style', 'opacity', 0),
            ('id', 'style', 'opacity', 0),
        )
    step = 0.33
    steps = step * fps
    frames = int(4 * steps)
    for i in range(0, frames):
        yield (
            ('logo', 'attr', 'transform', f'translate(1550, 875) scale(.2,.2)'),
            ('title', 'style', 'opacity', easeInQuad(clamp(i, 0, fps), 0, 1, fps)),
            ('subtitle', 'style', 'opacity', easeInQuad(clamp(i - 1*steps, 0, fps), 0, 1, fps)),
            ('personnames', 'style', 'opacity', easeInQuad(clamp(i - 2*steps, 0, fps), 0, 1, fps)),
            ('id', 'style', 'opacity', easeInQuad(clamp(i - 3*steps, 0, fps), 0, 1, fps)),
        )
    frames = int(5*fps)
    for i in range(0, frames):
        yield (
            ('logo', 'attr', 'transform', f'translate(1550, 875) scale(.2,.2)'),
        )


def outroFrames(args):
#fadein outro graphics
    frames = 3*fps
    for i in range(0, frames):
        yield(())


def debug():
    render('divoc-hs-intro.svg',
        '../divoc-hs-intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'StageWar live! mit vielen Wörtern extra lang das wird jetzt echt zu viel extra lang das wird jetzt echt zu viel extra lang das wird jetzt echt zu viel',
            '$subtitle': 'Metal Konzert mit vielen Wörtern extra lang das wird jetzt echt zu viel extra lang das wird jetzt echt zu viel extra lang das wird jetzt echt zu viel',
            '$personnames':  'www.stagewar.de mit vielen Wörtern extra lang das wird jetzt echt zu viel extra lang das wird jetzt echt zu viel extra lang das wird jetzt echt zu viel'
        }
    )

    render('divoc-hs-outro.svg',
        '../divoc-hs-outro.ts',
        outroFrames
    )

    # render(
    #     'background.svg',
    #     '../background.ts',
    #     backgroundFrames
    # )
    #
    # render('pause.svg',
    #     '../pause.ts',
    #     pauseFrames
    # )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        # if event['room'] not in ('Chirurgie (Saal 1.04)', 'Kreißsaal (Saal 1.11)'):
        #     print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
        #     continue
        # if not (idlist==[]):
        #         if 000000 in idlist:
        #                 print("skipping id (%s [%s])" % (event['title'], event['id']))
        #                 continue
        #         if int(event['id']) not in idlist:
        #                 print("skipping id (%s [%s])" % (event['title'], event['id']))
        #                 continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'divoc-hs-intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$personnames': event['personnames']
            }
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'divoc-hs-outro.svg',
            outfile = 'divoc-hs-outro.ts',
            sequence = outroFrames
         ))
