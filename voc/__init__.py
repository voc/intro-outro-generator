#!/usr/bin/python3

from renderlib import *

def pauseFrames(p):
	# 5x logo
	times = 4
	for _ in range(0, times):
		frames = 10*fps
		for i in range(0, frames):
			yield (
				('pause2', 'attr',  'transform', 'translate(%.4f, 0)' % easeLinear(i, -1820, 1820+1060, frames)),
				('pause2', 'style', 'opacity', 1),
				('pause1', 'style', 'opacity', 0),
			)

	# 1x katze
	frames = 10*fps
	for i in range(0, frames):
		yield (
			('pause1', 'attr',  'transform', 'translate(%.4f, 0)' % easeLinear(i, -680, 680+1800, frames)),
			('pause1', 'style', 'opacity', 1),
			('pause2', 'style', 'opacity', 0),
		)

def debug():
	render(
		'pause.svg',
		'../pause.ts',
		pauseFrames
	)

	render(
		'pause.svg',
		'../pause.dv',
		pauseFrames
	)

def tasks(queue):
	raise NotImplementedError('call with --debug to render your intro/outro')
