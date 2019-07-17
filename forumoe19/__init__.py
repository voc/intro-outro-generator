#!/usr/bin/python

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://gist.githubusercontent.com/danimo/3cf27a2198da2fbc7c1fb138c13506ce/raw/forumoe19-schedule.xml'

personmap = {
1: 'Margit Stumpp (Fraktion B. 90/Die Grünen)',
2: 'Marja-Liisa Völlers (SPD-Fraktion)',
3: 'Dr. Jens Brandenburg (FDP-Fraktion)',
}

taglinemap = {
1: "Bildungspolitische Sprecherin",
2: "Expertin für frühk., schul. und berufl. Bildung",
3: "Sprecher für Studium und Bildung",
4: "mediale.pfade",
}


def bounce(i, min, max, frames):
    if i == frames - 1:
        return 0

    if i <= frames/2:
        return easeInOutQuad(i, min, max, frames/2)
    else:
        return max - easeInOutQuad(i - frames/2, min, max, frames/2)

def introFrames(parameters):
    # 1 Sekunde Text Fadein
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('text', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
        )

    # 4 Sekunden stehen lassen
    frames = 4*fps
    for i in range(0, frames):
        yield ()

def outroFrames(p):
    # 5 Sekunden stehen bleiben
    frames = 5*fps
    for i in range(0, frames):
        yield []

def bbFrames(parameters):
    # 1 Sekunde Text Fadein
    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('bg', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
            ('text', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames)),
        )

    # 3 Sekunden stehen lassen
    frames = 3*fps
    for i in range(0, frames):
        yield ()

    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('bg', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
            ('text', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
        )



def debug():
#    render(
#      'intro.svg',
#      '../intro.ts',
#      introFrames,
#      {
#          '$ID': 4711,
#          '$TITLE': "Long Long Long title is LONG",
#          '$SUBTITLE': 'Long Long Long Long subtitle is LONGER',
#          '$SPEAKER': 'Long Name of Dr. Dr. Prof. Dr. Long Long'
#      }
#    )

    render(
      'insert.svg',
      '../insert.mkv',
      bbFrames,
      {
          '$PERSON': "Prof. Bernhard Birnbaum",
          '$TAGLINE': "Leiter des rennomierten Birnbaum-Instituts",
      }
    )

#    render(
#        'pause.svg',
#        '../pause.ts',
#        pauseFrames
#    )
#
#    render(
#      'outro.svg',
#      '../outro.ts',
#      outroFrames
#    )

def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('ecdf'):
            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            continue
        if not (idlist==[]):
            if 000000 in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue
            if int(event['id']) not in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue

        # generate a task description and put it into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$ID': event['id'],
                '$TITLE': event['title'],
                '$SUBTITLE': event['subtitle'],
                '$SPEAKER': event['personnames']
                }
            ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

    for person in persons(scheduleUrl, personmap, taglinemap):
        queue.put(Rendertask(
            infile = 'insert.svg',
            outfile = "insert_{}.mkv".format(person['person'].replace("/", "_")),
            sequence = bbFrames,
            parameters = {
                '$PERSON': person['person'],
                '$TAGLINE': person['tagline'],
                }
            ))

