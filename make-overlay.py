#!/usr/bin/env python3
# vim: tabstop=4 shiftwidth=4 expandtab

import os
import sys
import subprocess
import argparse
import ssl
from configparser import ConfigParser
from pathlib import PurePath
import platform

from PIL import ImageFont
import schedulelib
ssl._create_default_https_context = ssl._create_unverified_context

FRAME_WIDTH = 1920


class TextConfig:
    x: int
    y: int

    fontfile_path: str
    fontsize: int
    fontcolor: str
    bordercolor: str = None  # border is added, if a color is set

    def uses_fontfile(self):
        return self.fontfile_path is not None

    def parse(self, cparser_sect, default_fontfile, default_fontcolor):
        self.x = cparser_sect.getint('x')
        self.y = cparser_sect.getint('y')
        self.width = cparser_sect.getint('width', FRAME_WIDTH-self.x-100)
        self.alignment = cparser_sect.get('alignment', 'left')

        if self.alignment not in ('left', 'center', 'right'):
            error(f"text alignment {self.alignment} unknown, must be left, right or center")

        self.fontcolor = cparser_sect.get('fontcolor', default_fontcolor)

        fontfile = cparser_sect.get('fontfile', default_fontfile)
        self.fontfile_path = str(PurePath(args.project, fontfile).as_posix())

        if not os.path.exists(self.fontfile_path):
            error("Font file {} in Project Path is missing".format(self.fontfile_path))

        self.fontsize = cparser_sect.getint('fontsize')
        self.bordercolor = cparser_sect.get('bordercolor', None)

    def fit_text(self, text: str) -> list[str]:
        if not text:
            return [(0, "")]

        font = ImageFont.truetype(
            self.fontfile_path, size=self.fontsize, encoding="unic")

        return fit_text(text, self.width, font)

    def get_ffmpeg_filter(self, text: list[str]):
        if not text:
            return ""

        filter_str = ""
        for idx, (line_width, line) in enumerate(text):
            line_x = self.x
            if self.alignment == "center":
                line_x = self.x + (self.width - line_width) / 2
            elif self.alignment == "right":
                line_x = self.x + (self.width - line_width)

            filter_str += "drawtext=box=1:boxcolor=black:x={}:y={}".format(
                line_x, self.y + (idx*self.fontsize))

            filter_str += ":fontfile='{}':fontsize={}:fontcolor={}:text={}".format(
                self.fontfile_path, self.fontsize, self.fontcolor, ffmpeg_escape_str(line))

            if self.bordercolor is not None:
                filter_str += ":borderw={}:bordercolor={}".format(
                    self.fontsize / 30, self.bordercolor)

            filter_str += ","

        return filter_str[:-1]


class Config:
    schedule: str
    template_file: str  # overlay template

    title: TextConfig
    speaker: TextConfig
    text: TextConfig
    extra_text: str = ""  # additional text


def parse_config(filename) -> Config:
    if not os.path.exists(filename):
        error("config.ini file in Project Path is missing")

    conf = Config()

    cparser = ConfigParser()
    cparser.read(filename)

    meta = cparser['meta']
    conf.schedule = meta.get('schedule')
    infile = PurePath(args.project, meta.get('template'))
    conf.template_file = str(infile)

    defaults = cparser['default']
    default_fontfile = defaults.get('fontfile', None)
    default_fontcolor = defaults.get('fontcolor', "#ffffff")

    conf.title = TextConfig()
    conf.title.parse(cparser['title'], default_fontfile, default_fontcolor)
    conf.speaker = TextConfig()
    conf.speaker.parse(cparser['speaker'], default_fontfile, default_fontcolor)
    conf.text = TextConfig()
    conf.text.parse(cparser['text'], default_fontfile, default_fontcolor)

    conf.extra_text = cparser['text'].get('text', '')

    if not os.path.exists(conf.template_file):
        error("Template file {} in Project Path is missing".format(conf.template_file))

    if not args.project:
        error("The Project Path is a required argument")

    if not args.debug and not conf.schedule:
        error("Either specify --debug or supply a schedule in config.ini")

    return conf


def error(err_str):
    print("##################################################")
    print(err_str)
    print("##################################################")
    print()
    parser.print_help()
    sys.exit(1)


def describe_event(event):
    return "#{}: {}".format(event['id'], event['title'])


def event_print(event, message):
    print("{} – {}".format(describe_event(event), message))


def fit_text(string: str, max_width: int, font: ImageFont) -> list[str]:
    """
        Break text into list of strings which fit certain a width (in pixels)
        for the specified font. Returns list of tulpes in format
        (width_px, text)
    """

    split_line = [x.strip() for x in string.split()]
    lines = []
    w = 0
    line = []
    for word in split_line:
        new_line = line + [word.rstrip(':')]
        w = font.getlength(" ".join(new_line))
        if w > max_width:
            lines.append((
                font.getlength(' '.join(line)),
                ' '.join(line),
            ))
            line = []

        line.append(word.rstrip(':'))

        #if word.endswith(':'):
        #    lines.append((
        #        font.getlength(' '.join(line)),
        #        ' '.join(line),
        #    ))
        #    line = []

    if line:
        lines.append((
            font.getlength(' '.join(line)),
            ' '.join(line),
        ))

    return lines


def ffmpeg_escape_str(text: str) -> str:
    # Escape according to https://ffmpeg.org/ffmpeg-filters.html#Notes-on-filtergraph-escaping
    # and don't put the string in quotes afterwards!
    text = text.replace(",", r"\,")
    text = text.replace(':', r"\\:")
    text = text.replace (';', r"\\\;")
    text = text.replace(']', r"\]")
    text = text.replace('[', r"\[")
    text = text.replace("'", r"\\\'")

    return text


def enqueue_job(conf: Config, event):
    event_id = str(event['id'])

    outfile = str(PurePath(args.project, 'event_' + event_id + '_persons' + '.png'))

    if event_id in args.skip:
        event_print(event, "skipping " + str(event['id']))
        return
    if os.path.exists(outfile) and not args.force:
        event_print(event, "file exist, skipping " + str(event['id']))
        return

    event_title = str(event['title'])
    event_personnames = str(event['personnames'])

    title = conf.title.fit_text(event_title)
    speakers = conf.speaker.fit_text(event_personnames)
    extra_text = conf.text.fit_text(conf.extra_text)

    if args.debug:
        print('Title:   ', title)
        print('Speaker: ', speakers)

    if platform.system() == 'Windows':
        ffmpeg_path = './ffmpeg.exe'
    else:
        ffmpeg_path = 'ffmpeg'

    videofilter = conf.title.get_ffmpeg_filter(title) + ","
    videofilter += conf.speaker.get_ffmpeg_filter(speakers) + ","
    videofilter += conf.text.get_ffmpeg_filter(extra_text)

    cmd = [ffmpeg_path, '-y', '-i', conf.template_file, '-frames:v', '1', '-vf', videofilter]

    cmd += ['-aspect', '16:9', '-f', 'image2', '-c', 'png', outfile]

    if args.debug:
        print(cmd)

    subprocess.check_call(cmd,
                          stderr=subprocess.STDOUT,
                          stdout=subprocess.DEVNULL
                          )

    return event_id


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='C3VOC Overlay Generator - Creates lower-thirds from schedule.xml',
        usage="./make-overlay.py yourproject/",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('project', action="store", metavar='Project folder', type=str, help='''
        Path to your project folder
        ''')

    parser.add_argument('--debug', action="store_true", default=False, help='''
        Run script in debug mode and render with placeholder texts,
        not parsing or accessing a schedule.
        This argument must not be used together with --id
        Usage: ./make-overlay.py yourproject/ --debug
        ''')

    parser.add_argument('--id', dest='ids', nargs='+', action="store", type=int, help='''
        Only render the given ID(s) from your projects schedule.
        This argument must not be used together with --debug
        Usage: ./make-overlay.py yourproject/ --id 4711 0815 4223 1337
        ''')

    parser.add_argument('--room', dest='rooms', nargs='+', action="store", type=str, help='''
        Only render the given room(s) from your projects schedule.
        This argument must not be used together with --debug
        Usage: ./make-overlay.py yourproject/ --room "HfG_Studio" "ZKM_Vortragssaal"
        ''')

    parser.add_argument('--skip', nargs='+', action="store", type=str, help='''
        Skip ID(s) not needed to be rendered.
        Usage: ./make-overlay.py yourproject/ --skip 4711 0815 4223 1337
        ''')

    parser.add_argument('--force', action="store_true", default=False, help='''
        Force render if file exists.
        ''')

    args = parser.parse_args()

    if (args.skip is None):
        args.skip = []

    config = parse_config(PurePath(args.project, 'config.ini'))

    if args.debug:
        persons = ['Kenneth Edwall', 'Anna Engström',]
        events = [{
            'id': 'debug',
            'title': "Sweden's Public Sector in Transition: Exploring Open Standards for Interoperable Communication",
            'persons': persons,
            'personnames': ', '.join(persons),
            'room': 'Ada Byron',
        }]

    else:
        events = list(schedulelib.events(config.schedule))

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

        job_id = enqueue_job(config, event)
        if not job_id:
            event_print(event, "job was not enqueued successfully, skipping postprocessing")
            continue

    print('all done')
