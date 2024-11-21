#!/usr/bin/env python3
# vim: tabstop=4 shiftwidth=4 expandtab

import schedulelib
import argparse
import tempfile
import shutil
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
parser.add_argument('schedule', action="store", metavar='Schedule-URL', type=str, nargs='?', help='''
    URL or Path to your schedule.xml
    ''')

parser.add_argument('--develop', action="store_true", default=False, help='''
    Run script in develop mode and render with placeholder texts,
    not parsing or accessing a schedule. Schedule-URL can be left blank when
    used with --develop
    This argument must not be used together with --id
    Usage: ./make.py yourproject/ --develop
    ''')

parser.add_argument('--id', dest='ids', nargs='+', action="store", type=int, help='''
    Only render the given ID(s) from your projects schedule.
    This argument must not be used together with --develop
    Usage: ./make.py yourproject/ --id 4711 0815 4223 1337
    ''')

parser.add_argument('--exclude-id', dest='exclude_ids', nargs='+', action="store", type=int, help='''
    Do not render the given ID(s) from your projects schedule.
    Usage: ./make.py yourproject/ --exclude-id 1 8 15 16 23 42
    ''')

parser.add_argument('--vcodec', type=str, default='mpeg2video', help='''
    ffmpeg video codec to use. defaults to mpeg2video, libx264 or copy (keeps the original h264 stream) is also often used.
    ''')

parser.add_argument('--acodec', type=str, default='mp2', help='''
    ffmpeg video codec to use. defaults to mp2, aac or copy (keeps the m4a stream) is also often used.
    ''')

parser.add_argument('--num-audio-streams', dest='naudio', type=int, default=1, help='''
    number of audio-streams to generate. defaults to 1
    ''')

parser.add_argument('--no-cleanup', action='store_true', help='''
    keep temp-dir for debugging purposes
    ''')

parser.add_argument('--snapshot-sec', type=int, default=3, help='''
    number of seconds into the final clip when to take a snapshot (for inspection purposes or as thumbnail)
    ''')

parser.add_argument('--setting-path', default='hd1080p.compressorsetting', help='''
    filename in the script-dir (where this python script resides),
    the work-dir (where the .motn-file resides) or absolute path to
    a .compressorsetting file
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

if not args.develop and not args.schedule:
    error("Either specify --develop or supply a schedule")

if args.develop:
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
    events = list(schedulelib.events(args.schedule))


def describe_event(event):
    return "#{}: {}".format(event['id'], event['title'])


def event_print(event, message):
    print("{} – {}".format(describe_event(event), message))

def find_settingpath():
    artwork_dir = os.path.dirname(args.motn)
    setting_path = os.path.join(artwork_dir, args.setting_path)
    if os.path.exists(setting_path):
        return setting_path

    setting_path = os.path.join(os.path.dirname(__file__), args.setting_path)
    if os.path.exists(setting_path):
        return setting_path

    return args.setting_path


tempdir = tempfile.TemporaryDirectory()
print('working in ' + tempdir.name)
settingpath = find_settingpath()


def fmt_command(command, **kwargs):
    args = {}
    for key, value in kwargs.items():
        args[key] = shlex.quote(value)

    return command.format(**args)


def run(command, **kwargs):
    os.system(fmt_command(command, **kwargs))


def run_output(command, **kwargs):
    # Apple Compressor behaves weirdly with its stdout. It will not terminate right when ran through
    # os.subprocess, but work fine when run via os.system. To still get the output, we pipe it into a
    # tempfile. This solution is quite stable.
    # see https://twitter.com/mazdermind/status/1588286020121870336
    with tempfile.NamedTemporaryFile() as t:
        cmd = fmt_command(command, **kwargs)
        os.system(f'{cmd} >{t.name} 2>&1')
        return t.read().decode('utf-8')


def enqueue_job(event):
    event_id = str(event['id'])
    work_doc = os.path.join(tempdir.name, event_id + '.motn')
    intermediate_clip = os.path.join(tempdir.name, event_id + '.mov')

    with open(args.motn, 'r') as fp:
        xmlstr = fp.read()

    for key, value in event.items():
        xmlstr = xmlstr.replace("$" + str(key), xmlescape(str(value)))

    with open(work_doc, 'w') as fp:
        fp.write(xmlstr)

    compressor_info = run_output(
        '/Applications/Compressor.app/Contents/MacOS/Compressor -batchname {batchname} -jobpath {jobpath} -settingpath {settingpath} -locationpath {locationpath}',
        batchname=describe_event(event),
        jobpath=work_doc,
        locationpath=intermediate_clip,
        settingpath=settingpath)

    match = re.search(r"<jobID ([A-Z0-9\-]+) ?\/>", compressor_info)
    if not match:
        event_print(event, "unexpected output from compressor: \n" + compressor_info)
        return

    return match.group(1)


def fetch_job_status():
    compressor_status = run_output(
        '/Applications/Compressor.app/Contents/MacOS/Compressor -monitor')
    job_status_matches = re.finditer(r"<jobStatus (.*) \/jobStatus>", compressor_status)

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
            event_print(event, "failed with staus=" + status +
                        " – removing from postprocessing queue")

    return new_active_jobs, finished_jobs


def finalize_job(job_id, event):
    event_id = str(event['id'])
    intermediate_clip = os.path.join(tempdir.name, event_id + '.mov')
    final_clip = os.path.join(os.path.dirname(args.motn), event_id + '.ts')
    copy_clip = os.path.join(os.path.dirname(args.motn), event_id + '.mov')
    snapshot_file = os.path.join(os.path.dirname(args.motn), event_id + '.png')

    shutil.copy(intermediate_clip, copy_clip)

    run('ffmpeg -y -hide_banner -loglevel error -i {input} -ar 48000 -ac 2 -map 0:v:0 -c:v {vcodec} -q:v 0 -aspect 16:9 '+(args.naudio * '-map 0:a:0 ')+' -c:a {acodec} -f mpegts {output}',
        input=intermediate_clip,
        output=final_clip,
        vcodec=args.vcodec,
        acodec=args.acodec)

    run('ffmpeg -y -hide_banner -loglevel error -i {input} -ss {snapshot_sec} -frames:v 1 -vf scale="iw*sar:ih" -f image2 -y -c png {output}',
        input=intermediate_clip,
        output=snapshot_file,
        snapshot_sec=str(args.snapshot_sec))

    event_print(event, "finalized intro to " + final_clip)


active_jobs = []

if args.ids:
    print("only including ids: ", args.ids)

if args.exclude_ids:
    print("excluding ids: ", args.exclude_ids)

filtered_events = events
filtered_events = filter(lambda event: not args.ids or event['id'] in args.ids, filtered_events)
filtered_events = filter(
    lambda event: not args.exclude_ids or event['id'] not in args.exclude_ids, filtered_events)
filtered_events = list(filtered_events)

print("enqueuing {} jobs into compressor".format(len(filtered_events)))
for event in filtered_events:
    job_id = enqueue_job(event)
    if not job_id:
        event_print(event, "job was not enqueued successfully, skipping postprocessing")
        continue

    event_print(event, "enqueued as " + job_id)
    active_jobs.append((job_id, event))

print("waiting for rendering to complete")

while len(active_jobs) > 0:
    time.sleep(10)
    active_jobs, finished_jobs = filter_finished_jobs(active_jobs)

    print("{} jobs in queue, {} ready to finalize".format(len(active_jobs), len(finished_jobs)))
    for job_id, event in finished_jobs:
        event_print(event, "finalizing job")
        finalize_job(job_id, event)


if args.no_cleanup:
    print('all done, *NOT* cleaning up, *TEMPFILES REMAIN* in ' + tempdir.name)

else:
    print('all done, cleaning up ' + tempdir.name)
    tempdir.cleanup()
