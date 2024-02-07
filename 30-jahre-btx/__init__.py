#!/usr/bin/python3

import svg.path, random
from lxml import etree
from renderlib import *
from schedulelib import *

def introFrames(p):
	frames = 0

	w = 1024
	rows = 16
	row_w = w / rows

	h = 576
	cols = 18
	col_h = h / cols

	yield (
		('colmask', 'style', 'fill', 'black'),
		('rowmask', 'style', 'fill', 'black'),
		('rowmask', 'attr', 'height', col_h),
	)

	for col in range(0, cols):
		for row in range(0, rows):
			yield (
				('colmask', 'attr', 'y', (col+1) * col_h),
				('colmask', 'attr', 'height', h - ((col+1) * col_h)),
				('rowmask', 'attr', 'y', col * col_h),
				('rowmask', 'attr', 'width', w - (row * row_w)),
			)

	frames = 2*fps
	for i in range(0, frames):
		yield (
			('colmask', 'attr', 'height', 0),
			('rowmask', 'attr', 'width', 0),
		)

def outroFrames(parameters):
	frames = int(0.5*fps)
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 0),
			('bar1', 'style', 'opacity', 0),
			('bar2', 'style', 'opacity', 0),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 0),
			('bar2', 'style', 'opacity', 0),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(0.5*fps)
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 1),
			('bar2', 'style', 'opacity', 0),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(0.5*fps)+1
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 1),
			('bar2', 'style', 'opacity', 1),
			('bar3', 'style', 'opacity', 0),
		)

	frames = int(3.5*fps)
	for i in range(0, frames):
		yield (
			('license', 'style', 'opacity', 1),
			('bar1', 'style', 'opacity', 1),
			('bar2', 'style', 'opacity', 1),
			('bar3', 'style', 'opacity', 1),
		)

def debug():
	render('intro.svg',
		'../intro.dv',
		introFrames
	)

	# render('outro.svg',
	# 	'../outro.dv',
	# 	outroFrames
	# )
