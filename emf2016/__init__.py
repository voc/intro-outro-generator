#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://www.emfcamp.org/schedule.frab'

titlemap = {
	1533: "Building applications with FOSS4G bricks"
}

def introFrames(p):
	move=50

	nr = p['$id'];


	# Hold still
	frames = 5*fps
	for i in range(0, frames):
		yield ()

	# 1s fade out
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('text', 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
		)

	# final frames
	for i in range(0,5):
		yield (
			('text', 'style',    'opacity', "%.4f" % 0),
		)

def outroFrames(p):
	# 3 Sekunden animation bleiben
	frames = 5*fps

	# five initial frames
	for i in range(0, 5):
		yield (
			('g1', 'style',    'opacity', "%.4f" % 0),
			('g2', 'style',    'opacity', "%.4f" % 0),
			('g3', 'style',    'opacity', "%.4f" % 0),
		)

	# 3 Sekunden
	frames = 6*fps
	for i in range(0, frames):
		yield (
			('g1', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 0*fps, i, 0, 1, 4*fps)),
			('g2', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 1*fps, i, 0, 1, 4*fps)),
			('g3', 'style',    'opacity', "%.4f" % easeDelay(easeLinear, 2*fps, i, 0, 1, 4*fps)),
		)

	# five final frames
	for i in range(0, 5):
		yield (
			('g1', 'style',    'opacity', "%.4f" % 1),
			('g2', 'style',    'opacity', "%.4f" % 1),
			('g3', 'style',    'opacity', "%.4f" % 1),
		)

def pauseFrames(p):
	# 3 Sekunden animation bleiben

	for nr in range(0, 3):
		# 10 sekunden sehen
		frames = 3*fps
		for i in range(0, frames):
			yield (
				('image%u' % ((nr+0)%3), 'style',    'opacity', "%.4f" % 1),
				('image%u' % ((nr+1)%3), 'style',    'opacity', "%.4f" % 0),
				('image%u' % ((nr+2)%3), 'style',    'opacity', "%.4f" % 0),
			)

		# 1 sekunde faden
		frames = 2*fps
		for i in range(0, frames):
			yield (
				('image%u' % ((nr+0)%3), 'style',    'opacity', "%.4f" % easeLinear(i, 1, -1, frames)),
				('image%u' % ((nr+1)%3), 'style',    'opacity', "%.4f" % easeLinear(i, 0, +1, frames)),
				('image%u' % ((nr+2)%3), 'style',    'opacity', "%.4f" % 0),
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

#	render(
#		'outro.svg',
#		'../outro.ts',
#		outroFrames
#	)
#
#	render(
#		'pause.svg',
#		'../pause.ts',
#		pauseFrames
#	)

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
