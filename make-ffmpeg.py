#!/usr/bin/env python3
# vim: tabstop=4 shiftwidth=4 expandtab

import os
import sys
import subprocess
import renderlib
import argparse
import shlex
from PIL import ImageFont
from configparser import ConfigParser
import json
import platform
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Parse arguments
parser = argparse.ArgumentParser(
    description='C3VOC Intro-Outro-Generator - Variant which renders only using video filters in ffmpeg',
    usage="./make-ffmpeg.py yourproject/",
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('project', action="store", metavar='Project folder', type=str, help='''
    Path to your project folder
    ''')

parser.add_argument('--debug', action="store_true", default=False, help='''
    Run script in debug mode and render with placeholder texts,
    not parsing or accessing a schedule.
    This argument must not be used together with --id
    Usage: ./make-ffmpeg.py yourproject/ --debug
    ''')

parser.add_argument('--id', dest='ids', nargs='+', action="store", type=int, help='''
    Only render the given ID(s) from your projects schedule.
    This argument must not be used together with --debug
    Usage: ./make-adobe-after-effects.py yourproject/ --id 4711 0815 4223 1337
    ''')

parser.add_argument('--room', dest='rooms', nargs='+', action="store", type=str, help='''
    Only render the given room(s) from your projects schedule.
    This argument must not be used together with --debug
    Usage: ./make-adobe-after-effects.py yourproject/ --room "HfG_Studio" "ZKM_Vortragssaal"
    ''')

parser.add_argument('--skip', nargs='+', action="store", type=str, help='''
    Skip ID(s) not needed to be rendered.
    Usage: ./make-ffmpeg.py yourproject/ --skip 4711 0815 4223 1337
    ''')

parser.add_argument('--force', action="store_true", default=False, help='''
    Force render if file exists.
    ''')

args = parser.parse_args()

if (args.skip is None):
	args.skip = []


def headline(str):
	print("##################################################")
	print(str)
	print("##################################################")
	print()


def error(str):
	headline(str)
	parser.print_help()
	sys.exit(1)

cparser = ConfigParser()
cparser.read(os.path.join(os.path.dirname(args.project), 'config.ini'))
template = cparser['default']['template']
alpha = cparser['default']['alpha']
prores = cparser['default']['prores']
fontfile = cparser['default']['fontfile'] # use a font file instead of a font family
inout = cparser['default']['inout'] # in and out time format: t for seconds, n for frame number

title_in = cparser['title']['in']
title_out = cparser['title']['out']
title_fontfamily = cparser['title']['fontfamily']
title_fontfile = cparser['title']['fontfile']
title_fontsize = cparser['title']['fontsize']
title_fontcolor = cparser['title']['fontcolor']
title_x = cparser['title']['x']
title_y = cparser['title']['y']

speaker_in = cparser['speaker']['in']
speaker_out = cparser['speaker']['out']
speaker_fontfamily = cparser['speaker']['fontfamily']
speaker_fontfile = cparser['speaker']['fontfile']
speaker_fontsize = cparser['speaker']['fontsize']
speaker_fontcolor = cparser['speaker']['fontcolor']
speaker_x = cparser['speaker']['x']
speaker_y = cparser['speaker']['y']

text_in = cparser['text']['in']
text_out = cparser['text']['out']
text_fontfamily = cparser['text']['fontfamily']
text_fontfile = cparser['text']['fontfile']
text_fontsize = cparser['text']['fontsize']
text_fontcolor = cparser['text']['fontcolor']
text_x = cparser['text']['x']
text_y = cparser['text']['y']
text_text = cparser['text']['text']

font_t = os.path.join(os.path.dirname(args.project), title_fontfile)
font_s = os.path.join(os.path.dirname(args.project), speaker_fontfile)
font_tt = os.path.join(os.path.dirname(args.project), text_fontfile)

fileformat = os.path.splitext(template)[1]
infile = os.path.join(os.path.dirname(args.project), template)

schedule = cparser['default']['schedule']

if not (os.path.exists(os.path.join(args.project, template))):
    error("Template file {} in Project Path is missing".format(template))

for ffile in (title_fontfile, speaker_fontfile, text_fontfile):
    if not (os.path.exists(os.path.join(args.project, ffile))):
        error("Font file {} in Project Path is missing".format(ffile))

if not (os.path.exists(os.path.join(args.project, 'config.ini'))):
    error("config.ini file in Project Path is missing")

if alpha == 'true' and not fileformat == '.mov':
    error("Alpha can only be rendered with .mov source files")

if not args.project:
    error("The Project Path is a required argument")

if not args.debug and not schedule:
    error("Either specify --debug or supply a schedule in config.ini")

if args.debug:
    persons = ['Thomas Roth', 'Dmitry Nedospasov', 'Josh Datko',]
    events = [{
        'id': 'debug',
        'title': 'wallet.fail',
        'subtitle': 'Hacking the most popular cryptocurrency hardware wallets',
        'persons': persons,
        'personnames': ', '.join(persons),
        'room': 'Borg',
    }]

else:
    events = list(renderlib.events(schedule))

def describe_event(event):
    return "#{}: {}".format(event['id'], event['title'])


def event_print(event, message):
    print("{} – {}".format(describe_event(event), message))


def fmt_command(command, **kwargs):
    args = {}
    for key, value in kwargs.items():
        args[key] = shlex.quote(value)

    command = command.format(**args)
    return shlex.split(command)


def run(command, **kwargs):
    return subprocess.check_call(
        fmt_command(command, **kwargs),
        stderr=subprocess.STDOUT,
        stdout=subprocess.DEVNULL)


def fit_text(string: str, frame_width):
    split_line = [x.strip() for x in string.split()]
    lines = ""
    w = 0
    line_num = 0
    line = ""
    for word in split_line:
        left, top, right, bottom = translation_font.getbbox(" ".join([line, word]))
        width, height = right - left, bottom - top
        if width > (frame_width - (2 * 6)):
            lines += line.strip() + "\n"
            line = ""

        line += word + " "

    lines += line.strip()
    return lines


def fit_title(string: str):
    global translation_font
    translation_font = ImageFont.truetype(
    font_t, size=80, encoding="unic")
    title = fit_text(string, 1080)

    return title


def fit_speaker(string: str):
    global translation_font
    translation_font = ImageFont.truetype(
    font_s, size=50, encoding="unic")
    speaker = fit_text(string, 1080)

    return speaker


def enqueue_job(event):
    event_id = str(event['id'])
    if event_id in args.skip:
        event_print(event, "skipping " + str(event['id']))
        return
    if (os.path.exists(os.path.join(args.project, event_id + '.ts')) or os.path.exists(os.path.join(args.project, event_id + '.mov'))) and not args.force:
        event_print(event, "file exist, skipping " + str(event['id']))
        return

    event_title = str(event['title'])
    event_personnames = str(event['personnames'])
    event_title = event_title.replace('"', '\\"')
    event_title = event_title.replace('\'', '')
    event_personnames = event_personnames.replace('"', '\\"')

    t = fit_title(event_title)
    t = t.replace(':', "\:") # the ffmpeg command needs colons to be escaped
    s = fit_speaker(event_personnames)

    if args.debug:
        print('Title: ', t)
        print('Speaker: ', s)

    outfile = os.path.join(os.path.dirname(args.project), event_id + '.ts')

    if platform.system() == 'Windows':
        ffmpeg_path = './ffmpeg.exe'
        font_t_win = "/".join(font_t.split("\\"))
        font_s_win = "/".join(font_s.split("\\"))
        font_tt_win = "/".join(font_tt.split("\\"))     
    else:
        ffmpeg_path  = 'ffmpeg'

    if fontfile == 'true':
        if platform.system() == 'Windows':
            videofilter = "drawtext=enable='between({8},{0},{1})':fontfile='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}',".format(title_in, title_out, font_t_win, title_fontsize, title_fontcolor, title_x, title_y, t, inout)
            videofilter += "drawtext=enable='between({8},{0},{1})':fontfile='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}':box=1,".format(speaker_in, speaker_out, font_s_win, speaker_fontsize, speaker_fontcolor, speaker_x, speaker_y, s, inout)
            videofilter += "drawtext=enable='between({8},{0},{1})':fontfile='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}'".format(text_in, text_out, font_tt_win, text_fontsize, text_fontcolor, text_x, text_y, text_text, inout)
        else:
            videofilter = "drawtext=enable='between({8},{0},{1})':fontfile='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}',".format(title_in, title_out, font_t, title_fontsize, title_fontcolor, title_x, title_y, t, inout)
            videofilter += "drawtext=enable='between({8},{0},{1})':fontfile='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}':box=1,".format(speaker_in, speaker_out, font_s, speaker_fontsize, speaker_fontcolor, speaker_x, speaker_y, s, inout)
            videofilter += "drawtext=enable='between({8},{0},{1})':fontfile='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}'".format(text_in, text_out, font_tt, text_fontsize, text_fontcolor, text_x, text_y, text_text, inout)
    else:
        videofilter = "drawtext=enable='between({8},{0},{1})':font='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}',".format(title_in, title_out, title_fontfamily, title_fontsize, title_fontcolor, title_x, title_y, t, inout)
        videofilter += "drawtext=enable='between({8},{0},{1})':font='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}':box=1,".format(speaker_in, speaker_out, speaker_fontfamily, speaker_fontsize, speaker_fontcolor, speaker_x, speaker_y, s, inout)
        videofilter += "drawtext=enable='between({8},{0},{1})':font='{2}':fontsize={3}:fontcolor={4}:x={5}:y={6}:text='{7}'".format(text_in, text_out, text_fontfamily, text_fontsize, text_fontcolor, text_x, text_y, text_text, inout)


    if fileformat == '.mov':
        if alpha == 'true':
            if prores == 'true':
                cmd = '{3} -y -i "{0}" -vf "{1}" -vcodec prores_ks -pix_fmt yuva444p10le -profile:v 4444 -shortest -movflags faststart -f mov "{2}"'.format(infile, videofilter, outfile, ffmpeg_path)
            else:
                cmd = '{3} -y -i "{0}" -vf "{1}" -shortest -c:v qtrle -movflags faststart -f mov "{2}"'.format(infile, videofilter, outfile, ffmpeg_path)
        else:
            cmd = '{3} -y -i "{0}" -vf "{1}" -map 0:0 -c:v mpeg2video -q:v 2 -aspect 16:9 -map 0:1 -c:a mp2 -b:a 384k -shortest -f mpegts "{2}"'.format(infile, videofilter, outfile, ffmpeg_path)
    else:
        cmd = '{3} -y -i "{0}" -vf "{1}" -map 0:0 -c:v mpeg2video -q:v 2 -aspect 16:9 -map 0:1 -c:a mp2 -b:a 384k -shortest -f mpegts "{2}"'.format(infile, videofilter, outfile, ffmpeg_path)

    if args.debug:
        print(cmd)

    run(cmd)

    return event_id


if args.ids:
    if len(args.ids) == 1:
        print("enqueuing {} job".format(len(args.ids)))
    else:
        print("enqueuing {} jobs".format(len(args.ids)))
else:
    if len(events) == 1:
        print("enqueuing {} job".format(len(events)))
    else:
        print("enqueuing {} jobs".format(len(events)))


for event in events:
    if args.ids and event['id'] not in args.ids:
        continue

    if args.rooms and event['room'] not in args.rooms:
        print("skipping room %s (%s)" % (event['room'], event['title']))
        continue

    event_print(event, "enqueued as " + str(event['id']))

    job_id = enqueue_job(event)
    if not job_id:
        event_print(event, "job was not enqueued successfully, skipping postprocessing")
        continue


print('all done')


