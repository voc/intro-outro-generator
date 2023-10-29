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

fade_duration = 0.5

title_in = float(cparser['title']['in'])
title_out = float(cparser['title']['out'])
title_duration = title_out - title_in
title_font = cparser['title']['font']
title_fontsize = int(cparser['title']['fontsize'])
title_fontcolor = cparser['title']['fontcolor']
title_x = int(cparser['title']['x'])
title_y = int(cparser['title']['y'])

speaker_in = float(cparser['speaker']['in'])
speaker_out = float(cparser['speaker']['out'])
speaker_duration = speaker_out - speaker_in
speaker_font = cparser['speaker']['font']
speaker_fontsize = int(cparser['speaker']['fontsize'])
speaker_fontcolor = cparser['speaker']['fontcolor']
speaker_x = int(cparser['speaker']['x'])
speaker_y = int(cparser['speaker']['y'])

text_in = float(cparser['text']['in'])
text_out = float(cparser['text']['out'])
text_duration = text_out - text_in
text_font = cparser['text']['font']
text_fontsize = int(cparser['text']['fontsize'])
text_fontcolor = cparser['text']['fontcolor']
text_x = int(cparser['text']['x'])
text_y = int(cparser['text']['y'])
text_text = cparser['text']['text']

font_t = os.path.join(os.path.dirname(args.project), title_font)
font_s = os.path.join(os.path.dirname(args.project), speaker_font)
font_tt = os.path.join(os.path.dirname(args.project), text_font)

fileformat = os.path.splitext(template)[1]
infile = os.path.join(os.path.dirname(args.project), template)

schedule = cparser['default']['schedule']

if not (os.path.exists(os.path.join(args.project, template))):
    error("Template file {} in Project Path is missing".format(template))

for ffile in (title_font, speaker_font, text_font):
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
    persons = ['Thomas Roth', 'Dmitry Nedospasov', 'Josh Datko']
    events = [{
        'id': 'debug',
        'title': 'wallet.fail',
        'subtitle': 'Hacking the most popular cryptocurrency hardware wallets',
        'persons': persons,
        'personnames': ', '.join(persons),
        'room': 'Borg',
    }]

else:
    events = list(schedulelib.events(schedule))


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
        w, _ = translation_font.getsize(" ".join([line, word]))
        print("{}, {}".format(w, line))
        if w > (frame_width):
            print("too wide, breaking")
            lines += line.strip() + "\n"
            line = ""

        line += word + " "

    lines += line.strip()
    return lines


def fit_title(string: str):
    global translation_font
    translation_font = ImageFont.truetype(font_t, size=title_fontsize-10, encoding="unic")
    title = fit_text(string, 1080)

    return title


def fit_speaker(string: str):
    global translation_font
    translation_font = ImageFont.truetype(font_s, size=speaker_fontsize-10, encoding="unic")
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
    event_title = event_title.replace('"', '')
    event_title = event_title.replace('\'', '')
    event_personnames = event_personnames.replace('"', '')

    t = fit_title(event_title)
    s = fit_speaker(event_personnames)
    print(s)

    if args.debug:
        print('Title: ', t)
        print('Speaker: ', s)

    outfile = os.path.join(os.path.dirname(args.project), event_id + '.ts')

    videofilter = "drawtext=fontfile={fontfile}:fontsize={fontsize}:fontcolor={fontcolor}:x={x}:y={y}:text='{text}':".format(
        fontfile=font_t,
        fontsize=title_fontsize,
        fontcolor=title_fontcolor,
        x=title_x,
        y=title_y,
        text=t)
    videofilter += "alpha='if(lt(t,{fade_in_start_time}),0,if(lt(t,{fade_in_end_time}),(t-{fade_in_start_time})/{fade_duration},if(lt(t,{fade_out_start_time}),1,if(lt(t,{fade_out_end_time}),({fade_duration}-(t-{fade_out_start_time}))/{fade_duration},0))))',".format(
        fade_in_start_time=title_in,
        fade_in_end_time=title_in + fade_duration,
        fade_out_start_time=title_in + fade_duration + title_duration,
        fade_out_end_time=title_in + fade_duration + title_duration + fade_duration,
        fade_duration=fade_duration
    )
    videofilter += "drawtext=fontfile={fontfile}:fontsize={fontsize}:fontcolor={fontcolor}:x={x}:y={y}:text='{text}':".format(
        fontfile=font_s,
        fontsize=speaker_fontsize,
        fontcolor=speaker_fontcolor,
        x=speaker_x,
        y=speaker_y,
        text=s)
    videofilter += "alpha='if(lt(t,{fade_in_start_time}),0,if(lt(t,{fade_in_end_time}),(t-{fade_in_start_time})/{fade_duration},if(lt(t,{fade_out_start_time}),1,if(lt(t,{fade_out_end_time}),({fade_duration}-(t-{fade_out_start_time}))/{fade_duration},0))))',".format(
        fade_in_start_time=speaker_in,
        fade_in_end_time=speaker_in + fade_duration,
        fade_out_start_time=speaker_in + fade_duration + speaker_duration,
        fade_out_end_time=speaker_in + fade_duration + speaker_duration + fade_duration,
        fade_duration=fade_duration
    )
    videofilter += "drawtext=fontfile={fontfile}:fontsize={fontsize}:fontcolor={fontcolor}:x={x}:y={y}:text={text}:".format(
        fontfile=font_tt,
        fontsize=text_fontsize,
        fontcolor=text_fontcolor,
        x=text_x,
        y=text_y,
        text=text_text)
    videofilter += "alpha='if(lt(t,{fade_in_start_time}),0,if(lt(t,{fade_in_end_time}),(t-{fade_in_start_time})/{fade_duration},if(lt(t,{fade_out_start_time}),1,if(lt(t,{fade_out_end_time}),({fade_duration}-(t-{fade_out_start_time}))/{fade_duration},0))))'".format(
        fade_in_start_time=text_in,
        fade_in_end_time=text_in + fade_duration,
        fade_out_start_time=text_in + fade_duration + text_duration,
        fade_out_end_time=text_in + fade_duration + text_duration + fade_duration,
        fade_duration=fade_duration
    )

    if fileformat == '.mov':
        if alpha == 'true':
            if prores == 'true':
                cmd = 'ffmpeg -y -i "{0}" -vf "{1}" -vcodec prores_ks -pix_fmt yuva444p10le -profile:v 4444 -shortest -movflags faststart -f mov "{2}"'.format(
                    infile, videofilter, outfile)
            else:
                cmd = 'ffmpeg -y -i "{0}" -vf "{1}" -shortest -c:v qtrle -movflags faststart -f mov "{2}"'.format(
                    infile, videofilter, outfile)
        else:
            cmd = 'ffmpeg -y -i "{0}" -vf "{1}" -map 0:0 -c:v mpeg2video -q:v 2 -aspect 16:9 -map 0:1 -c:a mp2 -b:a 384k -shortest -f mpegts "{2}"'.format(
                infile, videofilter, outfile)
    else:
        cmd = 'ffmpeg -y -i "{0}" -vf "{1}" -map 0:0  -c:v mpeg2video -pix_fmt:v yuv420p -qscale:v 2 -qmin:v 2 -qmax:v 7 -keyint_min 0 -bf 0 -g 0 -maxrate:0 90M  -aspect 16:9 -map 0:1 -c:a mp2 -b:a 384k -shortest -f mpegts "{2}"'.format(
            infile, videofilter, outfile)

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
