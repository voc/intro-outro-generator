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


class TextConfig:
    inpoint: float
    outpoint: float
    x: int
    y: int

    use_fontfile: bool
    fontfile: str
    fontfile_path: str
    fontfamily: str

    fontsize: int
    fontcolor: str = "#ffffff"

    def parse(self, cparser_sect, use_fontfile: bool):
        self.inpoint = cparser_sect.getfloat('in')
        self.outpoint = cparser_sect.getfloat('out')
        self.x = cparser_sect.getint('x')
        self.y = cparser_sect.getint('y')

        self.use_fontfile = use_fontfile
        if use_fontfile:
            self.fontfile = cparser_sect.get('fontfile')
            self.fontfile_path = str(PurePath(args.project, self.fontfile).as_posix())

            if not os.path.exists(self.fontfile_path):
                error("Font file {} in Project Path is missing".format(self.fontfile_path))
        else:
            self.fontfamily = cparser_sect.get('fontfamily')

        self.fontsize = cparser_sect.getint('fontsize')
        self.fontcolor = cparser_sect.get('fontcolor', self.fontcolor)

    def fit_text(self, text: str):
        global translation_font
        translation_font = ImageFont.truetype(
            self.fontfile_path, size=self.fontsize, encoding="unic")

        # TODO: Make this work with font family as well!

        return fit_text(text, (1920-self.x-100))

    def get_ffmpeg_filter(self, inout_type: str, text: str):
        filter_str = "drawtext=enable='between({},{},{})'".format(
            inout_type, self.inpoint, self.outpoint)

        if self.use_fontfile:
            filter_str += ":fontfile='{}'".format(self.fontfile_path)
        else:
            filter_str += ":font='{}'".format(self.fontfamily)

        filter_str += ":fontsize={0}:fontcolor={1}:x={2}:y={3}:text={4}".format(
            self.fontsize, self.fontcolor, self.x, self.y, ffmpeg_escape_str(text))

        return filter_str


class Config:
    schedule: str
    template_file: str  # video background
    alpha: bool = False
    prores: bool = False
    use_fontfile: bool = False
    inout_type: str = "t"  # in and out time format: t for seconds, n for frame number

    fileext: str

    title: TextConfig
    speaker: TextConfig
    text: TextConfig
    text_text: str = ""  # additional text


def parse_config(filename) -> Config:
    if not os.path.exists(filename):
        error("config.ini file in Project Path is missing")

    conf = Config()

    cparser = ConfigParser()
    cparser.read(filename)

    defaults = cparser['default']
    conf.schedule = defaults.get('schedule')
    infile = PurePath(args.project, defaults.get('template'))
    conf.template_file = str(infile)
    conf.alpha = defaults.getboolean('alpha', conf.alpha)
    conf.prores = defaults.getboolean('prores', conf.prores)
    conf.use_fontfile = defaults.get('fontfile', conf.use_fontfile)
    conf.inout_type = defaults.get('inout', conf.inout_type)

    conf.title = TextConfig()
    conf.title.parse(cparser['title'], conf.use_fontfile)
    conf.speaker = TextConfig()
    conf.speaker.parse(cparser['speaker'], conf.use_fontfile)
    conf.text = TextConfig()
    conf.text.parse(cparser['text'], conf.use_fontfile)

    conf.text_text = cparser['text'].get('text', '')

    conf.fileext = infile.suffix

    if not os.path.exists(conf.template_file):
        error("Template file {} in Project Path is missing".format(conf.template_file))

    if conf.alpha and conf.fileext != '.mov':
        error("Alpha can only be rendered with .mov source files")

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


def fit_text(string: str, frame_width):
    split_line = [x.strip() for x in string.split()]
    lines = ""
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


def ffmpeg_escape_str(text: str) -> str:
    # Escape according to https://ffmpeg.org/ffmpeg-filters.html#Notes-on-filtergraph-escaping
    # and don't put the string in quotes afterwards!
    text = text.replace(",", r"\,")
    text = text.replace(':', r"\\:")
    text = text.replace("'", r"\\\'")

    return text


def enqueue_job(conf: Config, event):
    event_id = str(event['id'])

    outfile = str(PurePath(args.project, event_id + '.ts'))
    outfile_mov = str(PurePath(args.project, event_id + '.mov'))

    if event_id in args.skip:
        event_print(event, "skipping " + str(event['id']))
        return
    if (os.path.exists(outfile) or os.path.exists(outfile_mov)) and not args.force:
        event_print(event, "file exist, skipping " + str(event['id']))
        return

    event_title = str(event['title'])
    event_personnames = str(event['personnames'])

    title = conf.title.fit_text(event_title)
    speakers = conf.speaker.fit_text(event_personnames)

    if args.debug:
        print('Title: ', title)
        print('Speaker: ', speakers)

    if platform.system() == 'Windows':
        ffmpeg_path = './ffmpeg.exe'
    else:
        ffmpeg_path = 'ffmpeg'

    videofilter = conf.title.get_ffmpeg_filter(conf.inout_type, title) + ","
    videofilter += conf.speaker.get_ffmpeg_filter(conf.inout_type, speakers) + ","
    videofilter += conf.text.get_ffmpeg_filter(conf.inout_type, conf.text_text)

    cmd = [ffmpeg_path, '-y', '-i', conf.template_file, '-vf', videofilter]

    if conf.fileext == '.mov' and conf.alpha:
        if conf.prores:
            cmd += ['-vcodec', 'prores_ks', '-pix_fmt', 'yuva444p10le', '-profile:v',
                    '4444', '-shortest', '-movflags', 'faststart', '-f', 'mov', outfile_mov]
        else:
            cmd += ['-shortest', '-c:v', 'qtrle', '-movflags',
                    'faststart', '-f', 'mov', outfile_mov]
    else:
        cmd += ['-map', '0:0', '-c:v', 'mpeg2video', '-q:v', '2', '-aspect', '16:9', '-map',
                '0:1', '-c:a', 'mp2', '-b:a', '384k', '-shortest', '-f', 'mpegts', outfile]

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

    config = parse_config(PurePath(args.project, 'config.ini'))

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
