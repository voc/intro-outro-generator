#!/usr/bin/env python3

import subprocess
import renderlib
import argparse
import tempfile
import shlex
import time
import sys
import os
import re

from xml.sax.saxutils import escape as xmlescape

# Parse arguments
parser = argparse.ArgumentParser(
	description='C3VOC Intro-Outro-Generator - Variant to use with apple Motion Files',
	usage="./make.py gpn17/Intro.motn https://url/to/schedule.xml",
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('motn', action="store", metavar='Motion-File', type=str, help='''
	Path to your Motion-File .motn-File
	''')
parser.add_argument('schedule', action="store", metavar='Schedule-URL', type=str,  nargs='?', help='''
	URL or Path to your schedule.xml
	''')

parser.add_argument('--debug', action="store_true", default=False, help='''
	Run script in debug mode and render with placeholder texts,
	not parsing or accessing a schedule. Schedule-URL can be left blank when
	used with --debug
	This argument must not be used together with --id
	Usage: ./make.py yourproject/ --debug
	''')

parser.add_argument('--id', dest='ids', nargs='+', action="store", type=int, help='''
	Only render the given ID(s) from your projects schedule.
	This argument must not be used together with --debug
	Usage: ./make.py yourproject/ --id 4711 0815 4223 1337
	''')

args = parser.parse_args()

def headline(str):
	print("##################################################")
	print(str)
	print("##################################################")
	print()

def error(str):
	headline(str)
	parser.print_help()
	sys.exit(1)

if not args.motn:
	error("The Motion-File is a rquired argument")

if not args.debug and not args.schedule:
	error("Either specify --debug or supply a schedule")

if args.debug:
	persons = ['Arnulf Christl', 'Astrid Emde', 'Dominik Helle', 'Till Adams']
	events = [{
		'id': 3773,
		'title': 'Was ist Open Source, wie funktioniert das?',
		'subtitle': 'Die Organisation der Open Geo- und GIS-Welt. Worauf man achten sollte.',
		'persons': persons,
		'personnames': ', '.join(persons),
		'room': 'Großer Saal',
	}]

else:
	events = list(renderlib.events(args.schedule))

def describe_event(event):
	return "#{}: {}".format(event['id'], event['title'])

def event_print(event, message):
	print("{} – {}".format(describe_event(event), message))

tempdir = tempfile.TemporaryDirectory()
print('working in '+tempdir.name)


def fmt_command(command, **kwargs):
	args = {}
	for key, value in kwargs.items():
		args[key] = shlex.quote(value)

	command = command.format(**args)
	return shlex.split(command)

def run(command, **kwargs):
	return subprocess.check_call(
		fmt_command(command, **kwargs))

def run_output(command, **kwargs):
	return subprocess.check_output(
		fmt_command(command, **kwargs),
		encoding='utf-8',
		stderr=subprocess.STDOUT)


def enqueue_job(event):
	event_id = str(event['id'])
	work_doc = os.path.join(tempdir.name, event_id+'.motn')
	intermediate_clip = os.path.join(tempdir.name, event_id+'.mov')

	with open(args.motn, 'r') as fp:
		xmlstr = fp.read()

	for key, value in event.items():
		xmlstr = xmlstr.replace("$"+str(key), xmlescape(str(value)))

	with open(work_doc, 'w') as fp:
		fp.write(xmlstr)

	compressor_info = run_output(
		'/Applications/Compressor.app/Contents/MacOS/Compressor -batchname {batchname} -jobpath {jobpath} -settingpath {home}/Library/Application\ Support/Compressor/Settings/Apple\ ProRes\ 4444.cmprstng -locationpath {locationpath}',
			batchname=describe_event(event),
			jobpath=work_doc,
			home=os.getenv('HOME'),
			locationpath=intermediate_clip)

	match = re.search("<jobID ([A-Z0-9\-]+) ?\/>", compressor_info)
	if not match:
		event_print(event, "unexpected output from compressor: \n"+compressor_info)
		return

	return match.group(1)

def fetch_job_status():
	compressor_status = run_output('/Applications/Compressor.app/Contents/MacOS/Compressor -monitor')
	job_status_matches = re.finditer("<jobStatus (.*) \/jobStatus>", compressor_status)

	status_dict = {}
	for match in job_status_matches:
		lexer = shlex.shlex(match.group(1), posix=True)
		lexer.wordchars += "="

		job_status = dict(word.split("=", maxsplit=1) for word in lexer)
		job_id = job_status['jobid']
		status_dict[job_id] = job_status

	return status_dict




def filter_finished_jobs(active_jobs):
	job_status = fetch_job_status()

	new_active_jobs = []
	finished_jobs = []
	for job_id, event in active_jobs:
		if job_id not in job_status:
			status = 'Processing'
		else:
			status = job_status[job_id]['status']

		if status == 'Processing':
			new_active_jobs.append((job_id, event))
			continue
		elif status == 'Successful':
			finished_jobs.append((job_id, event))
		else:
			event_print(event, "failed with staus="+status+" – removing from postprocessing queue")

	return new_active_jobs, finished_jobs


def finalize_job(job_id, event):
	event_id = str(event['id'])
	intermediate_clip = os.path.join(tempdir.name, event_id+'.mov')
	final_clip = os.path.join(os.path.dirname(args.motn), event_id+'.ts')

	run('ffmpeg -y -hide_banner -loglevel error -i "{input}" -ar 48000 -ac 1 -f s16le -i /dev/zero -map 0:v -c:v mpeg2video -q:v 0 -aspect 16:9 -map 1:0 -map 1:0 -map 1:0 -map 1:0 -shortest -f mpegts "{output}"',
		input=intermediate_clip,
		output=final_clip)

	event_print(event, "finalized intro to "+final_clip)



active_jobs = []

print("enqueuing {} jobs into compressor", len(events))
for event in events:
	if args.ids and event['id'] not in args.ids:
		continue

	job_id = enqueue_job(event)
	if not job_id:
		event_print(event, "job was not enqueued successfully, skipping postprocessing")
		continue

	event_print(event, "enqueued as "+job_id)
	active_jobs.append((job_id, event))

print("waiting for rendering to complete")

while len(active_jobs) > 0:
	time.sleep(60)
	active_jobs, finished_jobs = filter_finished_jobs(active_jobs)

	print("{} jobs in queue, {} ready to finalize".format(len(active_jobs), len(finished_jobs)))
	for job_id, event in finished_jobs:
		event_print(event, "finalizing job")
		finalize_job(job_id, event)


print('all done, cleaning up '+tempdir.name)
tempdir.cleanup()
