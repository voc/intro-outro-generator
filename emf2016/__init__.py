#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://www.emfcamp.org/schedule.frab'

titlemap = {}

def introFrames(p):
	move=50

	nr = p['$id'];


	# Show Title
	frames = 5*fps
	for i in range(0, frames):
		yield (
			('sponsors', 'style',    'opacity', 0),
			('white', 'style',    'opacity', 0),
		)

	# Fade In Sponsor
	frames = int(fps/2)
	for i in range(0, frames):
		yield (
			('white', 'style',    'opacity', easeLinear(i, 0, 1, frames)),
			('sponsors', 'style',    'opacity', 0),
			('text', 'style',    'opacity', easeLinear(i, 1, 0, frames)),
			('bg', 'style',    'opacity', easeLinear(i, 1, 0, frames)),
		)
	
	frames = int(fps/2)
	for i in range(0, frames):
		yield (
			('white', 'style',    'opacity', 1),
			('sponsors', 'style',    'opacity', easeLinear(i, 0, 1, frames)),
			('text', 'style',    'opacity', 0),
			('bg', 'style',    'opacity',0),
		)
		
	# Show Sponsor
	frames = 5*fps
	for i in range(0, frames):
		yield (
			('white', 'style',    'opacity', 1),
			('sponsors', 'style',    'opacity', 1),
			('text', 'style',    'visibility', 0),
			('bg', 'style',    'visibility', 0),
		)



def outroFrames(p):
	# hold slide for 5s
	frames = 5*fps
	for i in range(0, frames):
		yield (
		)

def pauseFrames(p):
	# hold slide for 5s
	frames = 5*fps
	for i in range(0, frames):
		yield (
		)

def debug():
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$id': 69,
			'$title': 'How To Make "Your Mum" Jokes Successfully',
			'$subtitle': 'But not necessarily tastefully',
			'$personnames': 'Matt Gray'
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

	render(
		'pause.svg',
		'../pause.ts',
		pauseFrames
	)

def tasks(queue, args):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl, titlemap):

		# generate a task description and put them into the queue
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
				'$id': event['id'],
				'$title': event['title'],
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames']
			}
		))
