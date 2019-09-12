# vim: tabstop=4 shiftwidth=4 expandtab

import os
import sys
import re
import glob
import shutil
import errno
import subprocess
from svgtemplate import SVGTemplate
from lxml import etree
from urllib.request import urlopen
from wand.image import Image

# Frames per second. Increasing this renders more frames, the avconf-statements would still need modifications
fps = 25
debug = True
args = None

def loadProject(projectname):
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), projectname))
    return __import__(projectname)


def easeDelay(easer, delay, t, b, c, d, *args):
    if t < delay:
        return b

    if t - delay > d:
        return b + c

    return easer(t - delay, b, c, d, *args)


class Rendertask:
    def __init__(self, infile, parameters={}, outfile=None, workdir='.', sequence=None):
        if isinstance(infile, list):
            self.infile = infile[0]
            # self.audiofile = infile[1]
        else:
            self.infile = infile
            self.audiofile = None
        self.parameters = parameters
        self.outfile = outfile
        self.workdir = workdir
        self.sequence = sequence # deprecated, use animated()

    def animated(self, sequence):
        atask = self
        atask.sequence = sequence
        return atask

    def is_animated(self):
        return self.sequence != None

    def fromtupel(tuple):
        task = Rendertask(tuple[0], tuple[2], tuple[1])
        if len(tuple) > 3:
            task = task.animated(tuple[3])
        return task

    def ensure(input):
        if isinstance(input, tuple):
            return Rendertask.fromtupel(input)
        elif isinstance(input, Rendertask):
            return input
        else:
            return None

# try to create all folders needed and skip, they already exist
def ensurePathExists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


# remove the files matched by the pattern
def ensureFilesRemoved(pattern):
    for f in glob.glob(pattern):
        os.unlink(f)

def renderFrame(infile, task, outfile):
    width = 1920
    height = 1080
    if args.imagemagick:
        # invoke imagemagick to convert the generated svg-file into a png inside the .frames-directory
        with Image(filename=infile) as img:
            with img.convert('png') as converted:
                converted.save(filename=outfile)
    else:
        # invoke inkscape to convert the generated svg-file into a png inside the .frames-directory
        cmd = 'inkscape --export-background=white --export-background-opacity=0 --export-width={1} --export-height={2} --export-png="{3}" "{4}" 2>&1 >/dev/null'.format(task.workdir, width, height, outfile, infile)
        errorReturn = subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        if errorReturn != '':
            print("inkscape exitted with error\n" + errorReturn)
            # sys.exit(42)

def cachedRenderFrame(frame, frameNr, task, cache):
        skip_rendering = False
        # skip first n frames, to speed up rerendering during debugging
        if 'only_rerender_frames_after' in task.parameters:
            skip_rendering = (frameNr <= task.parameters['only_rerender_frames_after'])

        if args.skip_frames:
            skip_rendering = (frameNr <= args.skip_frames)

        if args.only_frame:
            skip_rendering = (frameNr != args.only_frame)

        # print a line for each and every frame generated
        if debug and not skip_rendering:
            print("frameNr {0:3d} => {1}".format(frameNr, frame))

        frame = tuple(frame)
        if frame in cache:
            if debug:
                print("cache hit, reusing frame {0}".format(cache[frame]))

            framedir = task.workdir + "/.frames/"
            shutil.copyfile("{0}/{1:04d}.png".format(framedir, cache[frame]), "{0}/{1:04d}.png".format(framedir, frameNr))

            return
        elif not skip_rendering:
            cache[frame] = frameNr

        svgfile = '{0}/.frames/{1:04d}.svg'.format(task.workdir, frameNr)

        with SVGTemplate(task, svgfile) as svg:
            svg.replacetext()
            svg.transform(frame)
            svg.write()

        outfile = '{0}/.frames/{1:04d}.png'.format(task.workdir, frameNr)
        renderFrame(svgfile, task, outfile)

        # increment frame-number
        frameNr += 1


def rendertask_image(task):
    with SVGTemplate(task) as svg:
        svg.replacetext()
        svgfile = svg.write()
    renderFrame(svgfile, task, task.outfile)

def rendertask_video(task):
    # iterate through the animation sequence frame by frame
    # frame is a ... tbd
    cache = {}
    for frameNr, frame in enumerate(task.sequence(task.parameters)):
        cachedRenderFrame(frame, frameNr, task, cache)

    if args.only_frame:
        task.outfile = '{0}.frame{1:04d}.png'.format(task.outfile, args.only_frame)

    # remove the dv/ts we are about to (re-)generate
    ensureFilesRemoved(os.path.join(task.workdir, task.outfile))

    if task.outfile.endswith('.png'):
        cmd = 'cd {0} && cp ".frames/{1:04d}.png" "{2}"'.format(task.workdir, args.only_frame, task.outfile)

    # invoke avconv aka ffmpeg and renerate a lossles-dv from the frames
    #  if we're not in debug-mode, suppress all output
    elif task.outfile.endswith('.ts'):
        cmd = 'cd {0} && '.format(task.workdir)
        cmd += 'ffmpeg -f image2 -i .frames/%04d.png '
        if task.audiofile is None:
            cmd += '-ar 48000 -ac 1 -f s16le -i /dev/zero -ar 48000 -ac 1 -f s16le -i /dev/zero '
        else:
            cmd += '-i {0} -i {0} '.format(task.audiofile)

        cmd += '-map 0:0 -c:v mpeg2video -q:v 2 -aspect 16:9 '

        if task.audiofile is None:
            cmd += '-map 1:0 -map 2:0 '
        else:
            cmd += '-map 1:0 -c:a copy -map 2:0 -c:a copy '
        cmd += '-shortest -f mpegts "{0}"'.format(task.outfile)
    elif task.outfile.endswith('.mov'):
        cmd = 'cd {0} && '.format(task.workdir)
        cmd += 'ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -f image2 -i .frames/%04d.png -r 25 -shortest -c:v qtrle -f mov "{0}"'.format(task.outfile)
    elif task.outfile.endswith('.mkv'):
        cmd = 'cd {0} && ffmpeg -ar 48000 -ac 2 -f s16le -i /dev/zero -f image2 -i .frames/%04d.png -aspect 16:9 -c copy -shortest "{1}"'.format(task.workdir, task.outfile)
    else:
        cmd = 'cd {0} && ffmpeg -ar 48000 -ac 2 -f s16le -i /dev/zero -f image2 -i .frames/%04d.png -target pal-dv -aspect 16:9 -shortest "{1}"'.format(task.workdir, task.outfile)

    if debug:
        print(cmd)

    r = os.system(cmd + ('' if debug else '>/dev/null 2>&1'))

    # as before, in non-debug-mode the thread-worker does all progress messages
    if debug:
        if r != 0:
            sys.exit()

def rendertask(task):
    global args
    # in debug mode we have no thread-worker which prints its progress
    if debug:
        print("generating {0} from {1}".format(task.outfile, task.infile))

    ## Hacky workaround: Fix this properly without breaking the
    ## support for partially rendered intros
    if True: #args.skip_frames and 'only_rerender_frames_after' not in task.parameters:
        if os.path.isdir(os.path.join(task.workdir, '.frames')):
            print("Removing", os.path.join(task.workdir, '.frames'))
            shutil.rmtree(os.path.join(task.workdir, '.frames'))

    # make sure a .frames-directory exists in out workdir
    ensurePathExists(os.path.join(task.workdir, '.frames'))

    if task.is_animated():
        rendertask_video(task)
    else:
        rendertask_image(task)

    if not debug:
        print("cleanup")

        # remove the generated svg
        ensureFilesRemoved(os.path.join(task.workdir, '.gen.svg'))



# Download the Events-Schedule and parse all Events out of it. Yield a tupel for each Event
def downloadSchedule(scheduleUrl):
    print("downloading schedule")

    # download the schedule
    response = urlopen(scheduleUrl)

    # read xml-source
    xml = response.read()

    # parse into ElementTree
    parser = etree.XMLParser(huge_tree=True)
    return etree.fromstring(xml, parser)

def persons(scheduleUrl, personmap={}, taglinemap={}):
    schedule = downloadSchedule(scheduleUrl)
    # iterate all days
    for day in schedule.iter('day'):
        # iterate all rooms
        for room in day.iter('room'):
            # iterate events on that day in this room
            for event in room.iter('event'):
                # aggregate names of the persons holding this talk
                persons_seen = []
                if event.find('persons') is not None:
                    for person in event.find('persons').iter('person'):
                        id = int(person.get("id"))
                        person = re.sub(r'\s+', ' ', person.text).strip()
                        match = re.search(r'\((.*?)\)', person)
                        tagline = ''
                        if not match is None:
                            tagline = match.group(1)
                            person = person.split(" (")[0]
                        if id in taglinemap:
                            tagline = taglinemap[id]
                        if id in personmap:
                            person = personmap[id]
                        if not id in persons_seen:
                            persons_seen.append(id)
                            yield {
                                'id': id,
                                'person': person,
                                'tagline': tagline
                            }

def events(scheduleUrl, titlemap={}):
    schedule = downloadSchedule(scheduleUrl)
    # iterate all days
    for day in schedule.iter('day'):
        # iterate all rooms
        for room in day.iter('room'):
            # iterate events on that day in this room
            for event in room.iter('event'):
                # aggregate names of the persons holding this talk
                personnames = []
                if event.find('persons') is not None:
                    for person in event.find('persons').iter('person'):
                        personname = re.sub(r'\s+', ' ', person.text).strip()
                        personnames.append(personname)

                id = int(event.get('id'))

                if id in titlemap:
                    title = titlemap[id]
                elif event.find('title') is not None and event.find('title').text is not None:
                    title = re.sub(r'\s+', ' ', event.find('title').text).strip()
                else:
                    title = ''

                if event.find('subtitle') is not None and event.find('subtitle').text is not None:
                    subtitle = re.sub(r'\s+', ' ', event.find('subtitle').text).strip()
                else:
                    subtitle = ''
                # yield a tupel with the event-id, event-title and person-names
                yield {
                    'day': day.attrib['index'],
                    'id': id,
                    'title': title,
                    'subtitle': subtitle,
                    'persons': personnames,
                    'personnames': ', '.join(personnames),
                    'room': room.attrib['name'],
                    'track': event.find('track').text,
		            #'url': event.find('url').text
                }


try:
    from termcolor import colored
except ImportError:
    def colored(str, col):
        return str
