#!/usr/bin/python

import subprocess
from renderlib import *

def pyconFrames(params):
	frames = 500
	for i in range(0, frames):
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "/home/peter/Downloads/ss_sz/SuperSource_SZ_1080_25p_%05d.png" % (i)),
		)


def debug():
	render(
		'pause.svg',
		'../pause.ts',
		pyconFrames
	)
