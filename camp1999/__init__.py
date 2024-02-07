#!/usr/bin/python3

from renderlib import *
from schedulelib import *

# URL to Schedule-XML
scheduleUrl = 'http://annaberg6.de/stuff/camp99/schedule.xml'


def introFrames(p):
	move=50

	for t in range(0, 12):
		yield (
			('rocket',  'style',    'opacity', "%.4f" % 0),
			('year',    'style',    'opacity', "%.4f" % 0),
			('content', 'style',    'opacity', "%.4f" % 0),
		)

	for t in range(0, 5*fps):
		yield (
			('rocket',  'style',    'opacity',   "%.4f" % easeDelay(easeLinear, 0*fps, t, 0, 1, 3*fps)),
			('year',    'style',    'opacity',   "%.4f" % easeDelay(easeLinear, 1*fps, t, 0, 1, 3*fps)),
			('year',    'attr',     'transform', "translate(%.4f, 0)" % easeDelay(easeOutQuad, 1*fps, t, -move, move, 3*fps)),
			('content', 'style',    'opacity',   "%.4f" % easeDelay(easeLinear, 2*fps, t, 0, 1, 3*fps)),
		)

	for t in range(0, 1*fps):
		yield (
			('rocket',  'style',    'opacity', "%.4f" % 1),
			('year',    'style',    'opacity', "%.4f" % 1),
			('content', 'style',    'opacity', "%.4f" % 1),
		)

	for t in range(0, 4*fps):
		yield (
			('rocket',  'style',    'opacity', "%.4f" % 1),
			('year',    'style',    'opacity',   "%.4f" % easeDelay(easeLinear, 0*fps, t, 1, -1, 3*fps)),
			('year',    'attr',     'transform', "translate(%.4f, 0)" % easeDelay(easeOutQuad, 0*fps, t, 0, move, 3*fps)),
			('content', 'style',    'opacity',   "%.4f" % easeDelay(easeLinear, 1*fps, t, 1, -1, 3*fps)),
		)


def outroFrames(p):
	for t in range(0, 4*fps):
		yield (
			('text',   'style',    'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, t, 1, -1, 3*fps)),
			('knoten', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 1*fps, t, 1, -1, 3*fps)),
		)

	for t in range(0, 1*fps):
		yield (
			('text',   'style',    'opacity', "%.4f" % 0),
			('knoten', 'style',    'opacity', "%.4f" % 0),
		)


def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		parameters={
			'$title': 'Careerpunks',
			'$person': 'Dave del Torto'
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

                queue.put(Rendertask(
                        infile = 'intro.svg',
                        outfile = str(event['id'])+".dv",
                        sequence = introFrames,
                        parameters = {
                                '$id': event['id'],
                                '$title': event['title'],
                                '$subtitle': event['subtitle'],
                                '$personnames': event['personnames'],
                                '$person': event['personnames']
                        }
                ))


def ticket(ticket):
	return Rendertask(
		infile = 'intro.svg',
		sequence = introFrames,
		parameters = {
			'$title': ticket.get('Fahrplan.Title'),
			'$person': ticket.get('Fahrplan.Person_list')
		}
	)
