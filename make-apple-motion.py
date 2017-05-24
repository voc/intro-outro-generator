#!/usr/bin/env python3

import renderlib
import argparse
import sys

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


for event in events:
	if args.ids and evenbt['id'] not in args.ids:
		continue

	print("rendering", event)

