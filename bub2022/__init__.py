#!/usr/bin/python3

from renderlib import *
from easing import *
import math
import logging

# URL to Schedule-XML
scheduleUrl = 'https://fahrplan22.bits-und-baeume.org/bitsundbaeume/schedule/export/schedule.xml'

# For (really) too long titles
titlemap = {
    #708: "Neue WEB-Anwendungen des LGRB Baden-Württemberg im Überblick"
}


def outroFrames(p):
    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('logo',   'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
            ('plate',  'style',    'opacity', 0),
        )

    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('logo',   'style',    'opacity', 1),
            ('plate',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
        )

    frames = 2*fps
    for i in range(0, frames):
        yield (
            ('logo',   'style',    'opacity', 1),
            ('plate',  'style',    'opacity', 1),
        )

def introFrames(p):
    frames = math.floor(1.5*fps)
    for i in range(0, frames):
        yield (
            ('header', 'attr',    'y',       1318),
            ('text',  'style',    'opacity', 0),
        )

    frames = 1*fps
    for i in range(0, frames):
        yield (
            ('text',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
        )

    frames = math.ceil(3.5*fps)
    for i in range(0, frames):
        yield (
            ('text',  'style',    'opacity', 1),
        )

def pauseFrames(p):
    pass


def srtip_event_title(event_title):
    if len(event_title) > 80:
        count = 0
        title = [] 
        for word in event_title.split(" "):
            word_len = len(word)
            if count + word_len < 80:
                count += word_len
                title.append(word)
                logging.info(count)
            else:
                title.append("...")
                break
        return " ".join(title)
    else:
        return event_title

def debug():
    render(
        'intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 19990,
            '$title': 'Ein creative commons Repository für medizinische Metadatenmodelle zur Harmonisierung der Gesundheitsversorgung (DE)',
            '$personnames': 'Max Blumenstock, Christian Niklas'
        }
    )
#    render(
#        'outro.svg',
#        '../outro.ts',
#        outroFrames
#    )




def tasks(queue, params, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        event_title = srtip_event_title(event['title'])

        if not (idlist==[]):
            if 000000 in idlist:
                print("skipping id (%s [%s])" % (event_title, event['id']))
                continue
            if int(event['id']) not in idlist:
                print("skipping id (%s [%s])" % (event_title, event['id']))
                continue

        # generate a task description and put them into the queue
        if int(event['id']) not in skiplist:
            queue.put(Rendertask(
                infile = 'intro.svg',
                outfile = str(event['id'])+".ts",
                sequence = introFrames,
                parameters = {
                    '$id': event['id'],
                    '$title': event_title,
                    '$personnames': event['personnames']
                }
            ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
        ))
