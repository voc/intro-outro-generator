#!/usr/bin/env python3

import subprocess
import renderlib
import argparse
import tempfile
import shlex
import time
import sys
import os

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

def error(str):
	print("##################################################")
	print(str)
	print("##################################################")
	print()
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
	events = renderlib.events(args.schedule)

def run_check(command, **kwargs):
	args = {}
	for key, value in kwargs.items():
		args[key] = shlex.quote(value)

	command = command.format(**args)
	print(" -> "+command)
	subprocess.check_call(shlex.split(command))

def render(event):
	with tempfile.TemporaryDirectory() as tempdir:
		work_doc = os.path.join(tempdir, "work.motn")
		intermediate_clip = os.path.join(tempdir, "intermediate.mov")
		final_clip = os.path.join(os.path.dirname(args.motn), str(event['id'])+'.ts')

		with open(args.motn, 'r') as fp:
			xmlstr = fp.read()

		for key, value in event.items():
			xmlstr = xmlstr.replace("$"+str(key), xmlescape(str(value)))

		with open(work_doc, 'w') as fp:
			fp.write(xmlstr)

		print("  generated work-document in " + work_doc + ", now starting compressor")
		run_check(
			'/Applications/Compressor.app/Contents/MacOS/Compressor -jobpath "{jobpath}" -settingpath {home}/Library/Application\ Support/Compressor/Settings/Apple\ ProRes\ 4444.cmprstng -locationpath "{locationpath}"',
				jobpath=work_doc,
				home=os.getenv('HOME'),
				locationpath=intermediate_clip)

		while True:
			ps = subprocess.check_output(shlex.split('ps aux')).decode('utf-8')

			pscnt = ps.count('compressord')
			if pscnt == 0:
				break

			print("  still "+str(pscnt)+" Compressor.app-processes running")
			time.sleep(5)


		print("  generated intermediate-clip in " + intermediate_clip + ", now starting transcoder")
		run_check(
			'ffmpeg -y -i "{input}" -ar 48000 -ac 1 -f s16le -i /dev/zero -map 0:0 -c:v mpeg2video -q:v 0 -aspect 16:9 -map 1:0 -map 1:0 -map 1:0 -map 1:0 -shortest -f mpegts "{output}"',
				input=intermediate_clip,
				output=final_clip)

		print("  transcoded final-clip to " + final_clip)



for event in events:
	if args.ids and event['id'] not in args.ids:
		continue

	print("rendering", event)
	render(event)

