#!/usr/bin/python3


from renderlib import *
from schedulelib import *
from easing import *
from collections import deque

# Please EDIT this URL for each local event of Jugend hackt! ### URL to Schedule-XML
scheduleUrl = 'https://gist.githubusercontent.com/danimo/9c4cd61461435791b205d2b0613ec6a9/raw/5456a77594917aa4f960a48204b580d838189405/schedule.xml'

# For (really) too long titles
titlemap = {
# 26: "VKS",
}

personmap = {
# 20 : "",
}

def introFrames(parameters):
	# 8 Sekunden

	# 2 Sekunden Fadein logo und icongroup
	frames = int(2*fps)
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('icongroup',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('alpaca',  'style',	'opacity', 0),
			('text-bg',  'style',	'opacity', 0),
			('projectname',  'style',	'opacity', 0),
			('prenames',  'style',	'opacity', 0),
		)

	# 1 Sekunden Fadein alpaca und text-bg
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', 1),
			('icongroup',  'style',	'opacity', 1),
			('alpaca',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('text-bg',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('projectname',  'style',	'opacity', 0),
			('prenames',  'style',	'opacity', 0),
		)

	# 5 Sekunden Fadein #hack hack hack# projectname + prenames DIREKT einblenden, weil die Schriftart sich nicht faden lässt
	frames = 5*fps
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', 1),
			('icongroup',  'style',	'opacity', 1),
			('alpaca',  'style',	'opacity', 1),
			('text-bg',  'style',	'opacity', 1),
			('projectname',  'style',	'opacity', 1),
			('prenames',  'style',	'opacity', 1),
		)

def outroFrames(parameters):
	# 5 Sekunden

	# 1 Sekunden Fadein logo
	frames = int(1*fps)
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('licensegroup',  'style',	'opacity', 0),
			('logogroup',  'style',	'opacity', 0),
		)

	# 1 Sekunden Fadein licensegroup
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', 1),
			('licensegroup',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
			('logogroup',  'style',	'opacity', 0),
		)

	# 1 Sekunden Fadein logogroup
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', 1),
			('licensegroup',  'style',	'opacity', 1),
			('logogroup',  'style',	'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

	# 2 Sekunden stehen bleiben
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('background',  'style',	'opacity', 1),
			('logo',  'style',	'opacity', 1),
			('licensegroup',  'style',	'opacity', 1),
			('logogroup',  'style',	'opacity', 1),
		)
def backgroundFrames(parameters):
	# 20 Sekunden

	# 10 Sekunden alpaca einblenden
	frames = 10*fps
	for i in range(0, frames):
		yield (
			('background', 'style',	'opacity', 1),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 0.25, 1, frames)),
		)

	# 10 Sekunden alpaca ausblenden
	frames = 10*fps
	for i in range(0, frames):
		yield (
			('background', 'style',	'opacity', 1),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 1, -0.75, frames)),
		)


def pauseFrames(parameters):
	# 6 Sekunden

	# 3 Sekunden alpaca einblenden
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('pause', 'style',	'opacity', "%.4f" % easeInCubic(i, 1, -0.75, frames)),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 0.25, 0.75, frames)),
		)

	# 3 Sekunden alpaca ausblenden
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('pause', 'style',	'opacity', "%.4f" % easeInCubic(i, 0.25, 0.75, frames)),
			('alpaca', 'style',	'opacity', "%.4f" % easeInCubic(i, 1, -0.75, frames)),
		)

def debug():
	s1 = 'Lorem, Ipsum, Ad Dolor... '
	s2 = 'Lorem, Ipsum, Ad Dolor, Sit, Nomen, Est, Omen, Urbi et Orbi... '
	render(
		'intro.svg',
		'../intro.ts',
		introFrames,
		{
			'$PROJECTNAME': s1.upper(),
			'$prenames': s2,
		}
	)

	render(
		'outro.svg',
		'../outro.ts',
		outroFrames
	)

#	render(
#		'background.svg',
#		'../background.ts',
#		backgroundFrames
#	)
#
#	render('pause.svg',
#		'../pause.ts',
#		pauseFrames
#	)
#
def tasks(queue, args, idlist, skiplist):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl):
		if not (idlist==[]):
			if 000000 in idlist:
				print("skipping id (%s [%s])" % (event['title'], event['id']))
				continue
			if int(event['id']) not in idlist:
				print("skipping id (%s [%s])" % (event['title'], event['id']))
				continue

		# generate a task description and put them into the queue
		projectname = event['title']
		id = event['id']
		queue.put(Rendertask(
			infile = 'intro.svg',
			outfile = str(event['id'])+".ts",
			sequence = introFrames,
			parameters = {
#				'$id': event['id'],
				'$PROJECTNAME': titlemap[id].upper() if id in titlemap else projectname.upper(),
#				'$subtitle': event['subtitle'],
				'$prenames': personmap[id] if id in personmap else event['personnames']
			}
		))

	# place a task for the outro into the queue
	queue.put(Rendertask(
		infile = 'outro.svg',
		outfile = 'outro.ts',
		sequence = outroFrames
	))
