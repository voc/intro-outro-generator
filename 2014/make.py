#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import glob
import os
import re
import shutil
import errno
import unicodedata
import urllib2
import xml.etree.ElementTree as ET
import textwrap
import tempfile
import threading
import multiprocessing
from threading import Thread, Lock
from Queue import Queue

# Debug rendert einen Vor- und einen Abspann
fps = 25
debug = ('--debug' in sys.argv)

reload(sys)
sys.setdefaultencoding('utf-8')

# t: current time, b: begInnIng value, c: change In value, d: duration
def easeOutCubic(t, b, c, d):
	t=float(t)/d-1
	return c*((t)*t*t + 1) + b

def ensure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

def ensure_files_removed(files):
	for f in glob.glob(files):
		os.unlink(f)

def slugify(value):
	"""
	Normalizes string, converts to lowercase, removes non-alpha characters,
	and converts spaces to hyphens.
	"""
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
	value = unicode(re.sub('[-\s]+', '-', value))
	return value




def abspannFrames():
	# 5 Sekunden

	# 2 Sekunden Fadein Text
	frame = 0
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, easeOutCubic(i, 0, 1, frames), 0)

	# 2 Sekunde Fadein Lizenz-Logo
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 1, float(i)/frames)

	# 1 Sekunde stehen bleiben
	frame = frame+i+1
	frames = 1*fps
	for i in range(0, frames):
		yield (frame+i, 1, 1)

def vorspannFrames():
	# 7 Sekunden

	# 2 Sekunden Text 1
	frame = 0
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, easeOutCubic(i, 0, 1, frames), easeOutCubic(i, 0, 1, frames), 0)

	# 1 Sekunde Fadeout Text 1
	frame = frame+i+1
	frames = 1*fps
	for i in range(0, frames):
		yield (frame+i, 1, 1-(float(i)/frames), 0)

	# 2 Sekunden Text 2
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 1, 0, easeOutCubic(i, 0, 1, frames))

	# 2 Sekunden stehen bleiben
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 1, 0, 1)

def pauseFrames():
	# 12 Sekunden

	# 2 Sekunden Text1 stehen
	frame = 0
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 1, 0)

	# 2 Sekunden Fadeout Text1
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 1-easeOutCubic(i, 0, 1, frames), 0)

	# 2 Sekunden Fadein Text2
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 0, easeOutCubic(i, 0, 1, frames))

	# 2 Sekunden Text2 stehen
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 0, 1)

	# 2 Sekunden Fadeout Text2
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, 0, 1-easeOutCubic(i, 0, 1, frames))

	# 2 Sekunden Fadein Text1
	frame = frame+i+1
	frames = 2*fps
	for i in range(0, frames):
		yield (frame+i, easeOutCubic(i, 0, 1, frames), 0)


def abspann(lizenz, workdir='artwork', outdir='..'):
	if debug:
		print "erzeuge Abspann"

	filename = os.path.join(outdir, 'abspann-{0}.mp4'.format(lizenz))

	ensure_path_exists(os.path.join(workdir, '.frames'))

	with open(os.path.join(workdir, 'abspann.svg'), 'r') as abspann_file:
		abspann = abspann_file.read()

	for (frameNr, opacity, opacityLizenz) in abspannFrames():
		if debug:
			print "frameNr {0:2d} => opacity {1:0.2f}, opacityLizenz {2:0.2f}".format(frameNr, opacity, opacityLizenz)

		pairs = \
			('%opacityLizenz', str(opacityLizenz)), \
			('%opacity', str(opacity)), \
			('%lizenz', lizenz), \
			('%workdir', os.path.realpath(workdir) )

		with open(os.path.join(workdir, '.gen.svg'), 'w') as gen_file:
			gen_abspann = reduce(lambda a, kv: a.replace(*kv), pairs, abspann)
			gen_file.write( gen_abspann )

		os.system('cd {0} && rsvg-convert .gen.svg > .frames/{1:04d}.png'.format(workdir, frameNr))

	ensure_files_removed(filename)
	os.system('cd {0} && avconv -f image2 -i .frames/%04d.png -c:v libx264 -preset veryslow -qp 0 "{1}"'.format(workdir, filename) + ('' if debug else '>/dev/null 2>&1'))

	if debug:
		print "aufräumen"
	shutil.rmtree(os.path.join(workdir, '.frames'))
	ensure_files_removed(os.path.join(workdir, '.gen.svg'))

def vorspann(id, title, personnames, workdir='artwork', outdir='..'):
	if debug:
		print u'erzeuge Vorspann für {0:4d} ("{1}")'.format(id, title)

	filename = os.path.join( outdir, u'{0:04d}-{1}.mp4'.format(id, slugify(unicode(title))) )

	ensure_path_exists(os.path.join(workdir, '.frames'))

	with open(os.path.join(workdir, 'vorspann.svg'), 'r') as vorspann_file:
		vorspann = vorspann_file.read()

	# svg does not have a method for automatic line breaking, that rsvg is capable of
	# so we do it in python as good as we can
	breaktitle = '</tspan><tspan x="150" dy="45">'.join(textwrap.wrap(title, 35))

	for (frameNr, opacityBox, opacity1, opacity2) in vorspannFrames():
		if debug:
			print "frameNr {0:2d} => opacityBox {1:0.2f}, opacity1 {2:0.2f}, opacity2 {3:0.2f}".format(frameNr, opacityBox, opacity1, opacity2)

		pairs = \
			('%opacity1', str(opacity1)), \
			('%opacity2', str(opacity2)), \
			('%opacityBox', str(opacityBox)), \
			('%id', str(id)), \
			('%title', breaktitle), \
			('%personnames', personnames), \
			('%workdir', os.path.realpath(workdir) )

		with open(os.path.join(workdir, '.gen.svg'), 'w') as gen_file:
			gen_vorspann = reduce(lambda a, kv: a.replace(*kv), pairs, vorspann)
			gen_file.write( gen_vorspann )

		os.system('cd {0} && rsvg-convert .gen.svg > .frames/{1:04d}.png'.format(workdir, frameNr))

	ensure_files_removed(filename)
	os.system(u'cd {0} && avconv -f image2 -i .frames/%04d.png -c:v libx264 -preset veryslow -qp 0 "{1}"'.format(workdir, filename) + ('' if debug else '>/dev/null 2>&1'))

	if debug:
		print "aufräumen"
	shutil.rmtree(os.path.join(workdir, '.frames'))
	ensure_files_removed(os.path.join(workdir, '.gen.svg'))

def pause(workdir='artwork', outdir='..'):
	if debug:
		print "erzeuge Pause-Loop"

	filename = os.path.join(outdir, 'pause.mp4')
	dvfilename = os.path.join(outdir, 'pause.dv')

	ensure_path_exists(os.path.join(workdir, '.frames'))

	with open(os.path.join(workdir, 'pause.svg'), 'r') as pause_file:
		pause = pause_file.read()

	for (frameNr, opacity1, opacity2) in pauseFrames():
		if debug:
			print "frameNr {0:2d} => opacity1 {1:0.2f}, opacity2 {2:0.2f}".format(frameNr, opacity1, opacity2)

		pairs = \
			('%opacity1', str(opacity1)), \
			('%opacity2', str(opacity2)), \
			('%workdir', os.path.realpath(workdir) )

		with open(os.path.join(workdir, '.gen.svg'), 'w') as gen_file:
			gen_pause = reduce(lambda a, kv: a.replace(*kv), pairs, pause)
			gen_file.write( gen_pause )

		os.system('cd {0} && rsvg-convert .gen.svg > .frames/{1:04d}.png'.format(workdir, frameNr))

	ensure_files_removed(filename)
	os.system('cd {0} && avconv -f image2 -i .frames/%04d.png -c:v libx264 -preset veryslow -qp 0 "{1}"'.format(workdir, filename) + ('' if debug else '>/dev/null 2>&1'))

	ensure_files_removed(dvfilename)
	os.system('cd {0} && avconv -f image2 -i .frames/%04d.png -target pal-dv "{1}"'.format(workdir, dvfilename) + ('' if debug else '>/dev/null 2>&1'))

	if debug:
		print "aufräumen"
	shutil.rmtree(os.path.join(workdir, '.frames'))
	ensure_files_removed(os.path.join(workdir, '.gen.svg'))


def events():
	print "downloading pentabarf schedule"
	response = urllib2.urlopen('http://www.fossgis.de/konferenz/2014/programm/schedule.de.xml')
	xml = response.read()
	schedule = ET.fromstring(xml)
	#schedule = ET.parse('schedule.de.xml')

	for day in schedule.iter('day'):
		date = day.get('date')
		for room in day.iter('room'):
			for event in room.iter('event'):
				personnames = []
				for person in event.find('persons').iter('person'):
					personnames.append(person.text)

				yield ( int(event.get('id')), event.find('title').text, ', '.join(personnames) )



if debug:
	print "!!! DEBUG MODE !!!"
	vorspann(667, 'OpenJUMP - Überblick, Neuigkeiten, Zusammenarbeit/Schnittstellen mit proprietärer Software', 'Matthias Scholz')
	abspann('by-sa')
	pause()
	sys.exit(0)




tasks = Queue()

for (id, title, personnames) in events():
	tasks.put( ('vorspann', id, title, personnames) )

tasks.put( ('abspann', 'by-sa') )
tasks.put( ('abspann', 'by-nc-sa') )
tasks.put( ('abspann', 'cc-zero') )
tasks.put( ('pause') )

num_worker_threads = multiprocessing.cpu_count()
print "{0} tasks in queue, starting {1} worker threads".format( tasks.qsize() - num_worker_threads, num_worker_threads )

for _ in range(num_worker_threads):
	tasks.put(None) # put sentinel to signal the end


printLock = Lock() 
def tprint(str):
	printLock.acquire()
	print threading.current_thread().name+': '+str
	printLock.release()



def worker():
	tempdir = os.path.join(tempfile.mkdtemp(), 'artwork')
	outdir = os.getcwd()

	tprint("initializing worker in {0}, writing result to {1}".format(tempdir, outdir))
	shutil.copytree('artwork', tempdir)

	while True:
		task = tasks.get()
		if task == None:
			break

		tprint( 'processing {0}'.format(task) )
		fnname = task[0]
		fn = globals()[fnname]
		opts = task[1:] + (tempdir, outdir)

		fn(*opts)
		tprint( 'finished {0}, {1} tasks left'.format(task, tasks.qsize() - num_worker_threads) )
		tasks.task_done()

	tprint("cleaning up worker")
	shutil.rmtree(tempdir)
	tasks.task_done()



for i in range(num_worker_threads):
	t = Thread(target=worker)
	t.daemon = True
	t.start()

tasks.join()
print "all worker threads ended"
