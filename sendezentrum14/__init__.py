#!/usr/bin/python3

from renderlib import *
from schedulelib import *
import math

def pauseFrames():
	# 7 Sekunden

	frames = 7*fps
	for i in range(0, frames):
		yield (
			('sun', 'attr', 'transform', "translate(625, 625) translate(-450, -375) rotate(%.4f) translate(-625, -625)" % (float(i)/float(frames)*30)),
		)

def debug():
	render(
		'pause.svg',
		'../pause.dv',
		pauseFrames
	)

	render(
		'nostream.svg',
		'../nostream.dv',
		pauseFrames
	)

	render(
		'novideo.svg',
		'../novideo.dv',
		pauseFrames
	)


def tasks(queue):
	# place the pause-sequence into the queue
	queue.put(Rendertask(
		infile = 'pause.svg',
		outfile = 'pause.dv',
		sequence = pauseFrames
	))

	queue.put(Rendertask(
		infile = 'nostream.svg',
		outfile = 'nostream.dv',
		sequence = pauseFrames
	))

	queue.put(Rendertask(
		infile = 'novideo.svg',
		outfile = 'novideo.dv',
		sequence = pauseFrames
	))
