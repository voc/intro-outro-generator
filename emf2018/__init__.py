#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'http://www.emfcamp.org/schedule.frab'

titlemap = {

}

def introFrames(p):
	givenFrame = 0

	nr = p['$id'];

	# 1 Sekunde nix 
	frames = 1*fps
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('layer1', 'style',    'opacity', "%.4f" % 0),  # nix 
			# ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
		)

	# 1 Sekunde Text Fadein
	frames = 1*fps
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('layer1', 'style',    'opacity', "%.4f" % easeInQuad(i, 0, 1, frames)),
			# ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
		)

	# 3 Sekunden Text
	frames = 3*fps
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('layer1', 'style',    'opacity', "%.4f" %1),
			# ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
		)
	
	# 1 Sekunde Text Fadeout
	frames = 1*fps
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('layer1', 'style',    'opacity', "%.4f" % easeInQuad(i, 1, -1, frames)),
			# ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
		)
		
	# Sponsors
	frames = 187
	for i in range(0, frames):
		givenFrame += 1
		yield (
			('bg',    'attr',  '{http://www.w3.org/1999/xlink}href', "given-frames/frame%04d.png" % (givenFrame)),
			('layer1', 'style',    'opacity', "0"),
			# ('text', 'attr',     'transform', 'translate(%.4f, 0)' % easeOutQuad(i, move, -move, frames)),
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
		'../intro.mov',
		 introFrames,
		{
			'$id': 42,
			'$title': 'Pan-Galactic Gargle Blaster',
			'$subtitle': 'the alcoholic equivalent of a mugging – expensive and bad for the head',
			'$personnames': 'Zaphod Beeblebrox',
			#'only_render_frame': 50
			#'only_rerender_frames_after': 120
		}
	)

	# render(
	#	'outro.svg',
	#	'../outro.ts',
	#	outroFrames
	# )

	# render(
	#	'pause.svg',
	#	'../pause.ts',
	#	pauseFrames
	# )

def tasks(queue, args, id_list, skip_list):
	# iterate over all events extracted from the schedule xml-export
	for event in events(scheduleUrl, titlemap):

		# skip events which will not be recorded
		#if event['room'] not in ('Saal A', 'Saal B') or event['track'] == 'Nomnom':
		#	print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
		#	continue

		# when id_list is not empty, only render events which are in id_list
		if id_list and int(event['id']) not in id_list:
			print("skipping id (%s [%s])" % (event['title'], event['id']))
			continue

		# generate a task description and put them into the queue
		queue.put(Rendertask(
			infile = ['intro.svg'],
			outfile = str(event['id']) + ".mov",
			sequence = introFrames,
			parameters = {
				'$id': event['id'],
				'$title': event['title'].upper(),
				'$subtitle': event['subtitle'],
				'$personnames': event['personnames'].upper(),
			}
		))
