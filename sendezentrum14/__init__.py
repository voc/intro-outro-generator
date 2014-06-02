#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
	queue.put((
		'pause.svg',
		'pause.dv',
		pauseFrames
	))

	queue.put((
		'nostream.svg',
		'nostream.dv',
		pauseFrames
	))

	queue.put((
		'novideo.svg',
		'novideo.dv',
		pauseFrames
	))
