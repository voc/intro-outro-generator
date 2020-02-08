#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from easing import *
import svg.path


personmap = {
}

taglinemap = {
}

# URL to Schedule-XML
scheduleUrl = 'https://fahrplan.events.ccc.de/congress/2019/Fahrplan/schedule.xml'


def tasks(queue, args, idlist, skiplist):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if event['room'] not in ('Ada', 'Borg', 'Clarke', 'Dijkstra', 'Eliza'):
			print("skipping room %s (%s)" % (event['room'], event['title']))
			continue

		if (event['id'] in idlist or not idlist):
			# generate a task description and put them into the queue
                        idx=0
                        for idx, person in enumerate(persons(scheduleUrl, personmap, taglinemap, event['id'])):
                            queue.put(Rendertask(
                                    infile = 'insert.svg',
                                    outfile = 'event_{}_person_{}.png'.format(str(event['id']), str(person['id'])),
                                    parameters = {
                                            '$person': person['person'],
                                            '$tagline': person['tagline'],
                                    }
                            ))

                            if idx > 0:
                                    queue.put(Rendertask(
                                    infile = 'insert.svg',
                                    outfile = 'event_{}_persons.png'.format(str(event['id'])),
                                    parameters = {
                                            '$person': event['personnames'],
                                            '$tagline': '',
                                    }
                            ))
