#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://pretalx.com/fossgis2022/schedule/export/schedule.xml'

def outroFrames(params):
	# 8 Sekunden

	# 2 Sekunden Fadein Text
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('banderole', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames) ),
			('license', 'style', 'opacity', 0)
		)

	# 2 Sekunde Fadein Lizenz-Logo
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('banderole', 'style', 'opacity', 1),
			('license', 'style', 'opacity', "%.4f" % (float(i)/frames))
		)

	# 4 Sekunde stehen bleiben
	frames = 4*fps
	for i in range(0, frames):
		yield (
			('banderole', 'style', 'opacity', 1),
			('license', 'style', 'opacity', 1)
		)

def introFrames(params):
	# 7 Sekunden

	# 2 Sekunden Text 1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box-und-text1',   'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
			('url',   'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
			('text1', 'style', 'opacity', "%.4f" % 1),
			('text2', 'style', 'opacity', 0)
		)

	# 1 Sekunde Fadeout Text 1
	frames = 1*fps
	for i in range(0, frames):
		yield (
			('box-und-text1',   'style', 'opacity', 1),
			('url',   'style', 'opacity', 1),
			('text1', 'style', 'opacity', "%.4f" % (1-(float(i)/frames))),
			('text2', 'style', 'opacity', 0)
		)

	# 2 Sekunden Text 2
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box-und-text1',   'style', 'opacity', 1),
			('url',   'style', 'opacity', 1),
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames))
		)

	# 2 Sekunden stehen bleiben
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('box-und-text1',   'style', 'opacity', 1),
			('url',   'style', 'opacity', 1),
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', 1)
		)

def pauseFrames(params):
	# 12 Sekunden

	# 2 Sekunden Text1 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 1),
			('text2', 'style', 'opacity', 0)
		)

	# 2 Sekunden Fadeout Text1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
			('text2', 'style', 'opacity', 0)
		)

	# 2 Sekunden Fadein Text2
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames))
		)

	# 2 Sekunden Text2 stehen
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', 1)
		)

	# 2 Sekunden Fadeout Text2
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', 0),
			('text2', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames)))
		)

	# 2 Sekunden Fadein Text1
	frames = 2*fps
	for i in range(0, frames):
		yield (
			('text1', 'style', 'opacity', "%.4f" % (easeOutCubic(i, 0, 1, frames))),
			('text2', 'style', 'opacity', 0)
		)

def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'StageWar live!',
            '$subtitle': 'Metal Konzert',
            '$persons':  'www.stagewar.de'
        }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )

    render('pause.svg',
        '../pause.ts',
        pauseFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Bühne 1', 'Bühne 2','Bühne 3','Bühne 4'):
            print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            continue
        if not (idlist==[]):
                if 000000 in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue
                if int(event['id']) not in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue

        # generate a task description and put them into the queue
        delimiter = ', '
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$persons': delimiter.join(event['persons']),
                '$url': event['url']
            }
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

    # place the pause-sequence into the queue
    if not "pause" in skiplist:
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
        ))

