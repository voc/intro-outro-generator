#!/usr/bin/env python3
# vim: tabstop=4 shiftwidth=4 expandtab

import subprocess
import renderlib
import argparse
import tempfile
import shlex
import time
import sys
import os
import platform
from shutil import copyfile

titlemap = {
    'id': "11404", 'title': "Attacking CPUs with Power Side Channels from Software",
    'id': "205", 'title': "Attacking CPUs with Power Side Channels from Software",
}

# Parse arguments
parser = argparse.ArgumentParser(
    description='C3VOC Intro-Outro-Generator - Variant to use with Blender Files',
    usage="./make-blender.py yourproject/ https://url/to/schedule.xml",
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('project', action="store", metavar='Project folder', type=str, help='''
    Path to your project folder with Blender Files (intro.blend)
    ''')
parser.add_argument('schedule', action="store", metavar='Schedule-URL', type=str, nargs='?', help='''
    URL or Path to your schedule.xml
    ''')

parser.add_argument('--debug', action="store_true", default=False, help='''
    Run script in debug mode and render with placeholder texts,
    not parsing or accessing a schedule. Schedule-URL can be left blank when
    used with --debug
    This argument must not be used together with --id
    Usage: ./make-blender.py yourproject/ --debug
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

parser.add_argument('--day', dest='days', nargs='+', action="store", type=str, help='''
    Only render from your projects schedule for the given days.
    This argument must not be used together with --debug
    Usage: ./make-adobe-after-effects.py yourproject/ --day "1" "3"
    ''')

parser.add_argument('--pause', action="store_true", default=False, help='''
    Render a pause loop from the pause.blend file in the project folder.
    ''')

parser.add_argument('--alpha', action="store_true", default=False, help='''
    Render intro/outro with alpha.
    ''')

parser.add_argument('--force', action="store_true", default=False, help='''
    Force render if file exists.
    ''')

parser.add_argument('--no-finalize', dest='nof', action="store_true", default=False, help='''
    Skip finalize job.
    ''')

parser.add_argument('--outro', action="store_true", default=False, help='''
    Render outro from the outro.blend file in the project folder.
    ''')

parser.add_argument('--bgloop', action="store_true", default=False, help='''
    Render background loop from the bgloop.blend file in the project folder.
    ''')

parser.add_argument('--keep', action="store_true", default=False, help='''
    Keep source file in the project folder after render.
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


if not args.project:
    error("The Path to your project with Blender Files is a required argument")

if not args.debug and not args.pause and not args.outro and not args.bgloop and not args.schedule:
    error("Either specify --debug, --pause, --outro or supply a schedule")

if args.debug:
    #persons = ['blubbel']
    persons = ['Vitor Sakaguti', 'Sara', 'A.L. Fehlhaber']
    events = [{
        'id': 11450,
        'title': 'PQ Mail: Enabling post quantum secure encryption for email communication',
        'subtitle': '',
        'persons': persons,
        'personnames': ', '.join(persons),
        'room': 'rc1',
    }]

elif args.pause:
    events = [{
        'id': 'pause',
        'title': 'Pause Loop',
    }]

elif args.outro:
    events = [{
        'id': 'outro',
        'title': 'Outro',
    }]

elif args.bgloop:
    events = [{
        'id': 'bgloop',
        'title': 'Background Loop',
    }]

else:
    events = list(renderlib.events(args.schedule))


def describe_event(event):
    return "#{}: {}".format(event['id'], event['title'])


def event_print(event, message):
    print("{} – {}".format(describe_event(event), message))


tempdir = tempfile.TemporaryDirectory()
print('working in ' + tempdir.name)


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


def run_show(command, **kwargs):
    return subprocess.check_call(
        fmt_command(command, **kwargs),
        stderr=subprocess.STDOUT)


def run_output(command, **kwargs):
    return subprocess.check_output(
        fmt_command(command, **kwargs),
        stderr=subprocess.STDOUT)


def enqueue_job(event):
    event_id = str(event['id'])
    if (os.path.exists(os.path.join(args.project, event_id + '.ts')) or os.path.exists(os.path.join(args.project, event_id + '.mkv'))) and not args.force:
        event_print(event, "file exist, skipping " + str(event['id']))
        return
    work_doc = os.path.join(tempdir.name, event_id + '.py')
    work_comp = os.path.join(args.project, event_id + '.blend')
    work_source = os.path.join(args.project, 'intro.blend')
    intermediate_clip = os.path.join(tempdir.name, event_id + '.mkv')

    if event_id == 'pause' or event_id == 'outro' or event_id == 'bgloop':
        copyfile(args.project + event_id + '.blend', work_doc)
        if platform.system() == 'Darwin':
            run(r'/Applications/Blender.app/Contents/MacOS/Blender --background {comp} --use-extension 1 --threads 0 --render-output {locationpath} --render-anim',
                comp=work_comp,
                locationpath=intermediate_clip)

        if platform.system() == 'Windows':
            run(r'C:/Program\ Files/Blender\ Foundation/Blender\ 2.91/blender.exe --background {comp} --use-extension 1 --threads 0 --render-output {locationpath} --render-anim',
                comp=work_comp,
                locationpath=intermediate_clip)
    else:
        with open(args.project + 'intro.py', 'r') as fp:
            scriptstr = fp.read()

        for key, value in event.items():
            value = str(value).replace('"', '\\"')
            scriptstr = scriptstr.replace("$" + str(key), value)
        
        with open(work_doc, 'w', encoding='utf-8') as fp:
            fp.write(scriptstr)
        
        if platform.system() == 'Darwin':
            run(r'/Applications/Blender.app/Contents/MacOS/Blender --background {source} --python-use-system-env --python {jobpath} --use-extension 1 --threads 0 --render-output {locationpath} --render-anim',
                source=work_source,
                jobpath=work_doc,
                locationpath=intermediate_clip)

        if platform.system() == 'Windows':
            run(r'C:/Program\ Files/Blender\ Foundation/Blender\ 2.91/blender.exe --background {source} --python-use-system-env --python {jobpath} --use-extension 1 --threads 0 --render-output {locationpath} --render-anim',
                source=work_source,
                jobpath=work_doc,
                locationpath=intermediate_clip)
    if args.debug or args.keep:
        copyfile(work_doc, args.project + event_id + '.py')

    return event_id


def finalize_job(job_id, event):
    event_id = str(event['id'])
    intermediate_clip = os.path.join(tempdir.name, event_id + '.mkv')
    final_clip = os.path.join(os.path.dirname(args.project), event_id + '.ts')

    if args.alpha:
        ffprobe = run_output('ffprobe -i {input} -show_streams -select_streams a -loglevel error',
            input=intermediate_clip)
        if ffprobe:
            run('ffmpeg -threads 0 -y -hide_banner -loglevel error -i {input} -c:v qtrle -movflags faststart -aspect 16:9 -c:a mp2 -b:a 384k -shortest -f mov {output}',
                input=intermediate_clip,
                output=final_clip)
        else:
            run('ffmpeg -threads 0 -y -hide_banner -loglevel error -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -i {input} -c:v qtrle -movflags faststart -aspect 16:9 -c:a mp2 -b:a 384k -shortest -f mov {output}',
                input=intermediate_clip,
                output=final_clip)
    else:
        ffprobe = run_output('ffprobe -i {input} -show_streams -select_streams a -loglevel error',
            input=intermediate_clip)
        if ffprobe:
            event_print(event, "finalize with audio from source file")
            run('ffmpeg -threads 0 -y -hide_banner -loglevel error -i {input} -c:v mpeg2video -q:v 2 -aspect 16:9 -c:a mp2 -b:a 384k -shortest -f mpegts {output}',
                input=intermediate_clip,
                output=final_clip)
        else:
            event_print(event, "finalize with silent audio")
            run('ffmpeg -threads 0 -y -hide_banner -loglevel error -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -i {input} -c:v mpeg2video -q:v 2 -aspect 16:9 -c:a mp2 -b:a 384k -shortest -f mpegts {output}',
                input=intermediate_clip,
                output=final_clip)

    if event_id == 'pause' or event_id == 'outro' or event_id == 'bgloop':
        event_print(event, "finalized " + str(event_id) + " to " + final_clip)
    else:
        event_print(event, "finalized intro to " + final_clip)


if args.ids:
    if len(args.ids) == 1:
        print("enqueuing {} job into aerender".format(len(args.ids)))
    else:
        print("enqueuing {} jobs into aerender".format(len(args.ids)))
else:
    if len(events) == 1:
        print("enqueuing {} job into aerender".format(len(events)))
    else:
        print("enqueuing {} jobs into aerender".format(len(events)))

for event in events:
    if args.ids and event['id'] not in args.ids:
        continue

    if args.rooms and event['room'] not in args.rooms:
        print("skipping room %s (%s)" % (event['room'], event['title']))
        continue

    if args.days and event['day'] not in args.days:
        print("skipping day %s (%s)" % (event['day'], event['title']))
        continue

    if str(event['id']) in str(titlemap['id']):
            event_print(event, "titlemap replacement")
            event['title'] = titlemap['title']

    event_print(event, "enqueued as " + str(event['id']))

    job_id = enqueue_job(event)
    if not job_id:
        event_print(event, "job was not enqueued successfully, skipping postprocessing")
        continue

    if not args.nof:
        event_print(event, "finalizing job")
        finalize_job(job_id, event)
    else:
        event_id = str(event['id'])
        event_print(event, "skipping finalizing job")
        if platform.system() == 'Windows':
            intermediate_clip = os.path.join(tempdir.name, event_id + '.avi')
            final_clip = os.path.join(os.path.dirname(args.project), event_id + '.avi')
        else:
            intermediate_clip = os.path.join(tempdir.name, event_id + '.mov')
            final_clip = os.path.join(os.path.dirname(args.project), event_id + '.mov')
        copyfile(intermediate_clip, final_clip)
        event_print(event, "copied intermediate clip to " + final_clip)

if args.debug or args.keep:
    print('keeping source files in ' + args.project)
else:
    print('all done, cleaning up ' + tempdir.name)
    tempdir.cleanup()
