# vim: tabstop=4 shiftwidth=4 expandtab

import re
from lxml import etree
from urllib.request import urlopen

scheduleTree = None


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


def getSchedule(scheduleUrl):
    global scheduleTree
    if not scheduleTree:
        scheduleTree = downloadSchedule(scheduleUrl)
    return scheduleTree


def persons(scheduleUrl, personmap={}, taglinemap={}, forEventId=None):
    schedule = getSchedule(scheduleUrl)
    # iterate all days
    for day in schedule.iter('day'):
        # iterate all rooms
        for room in day.iter('room'):
            # iterate events on that day in this room
            for event in room.iter('event'):
                eventid = int(event.get("id"))
                if event != None and not eventid == forEventId:
                    continue
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
    schedule = getSchedule(scheduleUrl)
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
                        try:
                            personname = re.sub(r'\s+', ' ', person.text).strip()
                        except:
                            personnames.append(str('None'))
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

                if event.find('url') is not None and event.find('url').text is not None:
                    url = event.find('url').text.strip()
                else:
                    url = ''
                # yield a tupel with the event-id, event-title and person-names
                yield {
                    'day': day.get('index'),
                    'id': id,
                    'title': title,
                    'subtitle': subtitle,
                    'persons': personnames,
                    'personnames': ', '.join(personnames),
                    'room': room.attrib['name'],
                    'track': event.find('track').text,
                    'url': url
                }


try:
    from termcolor import colored
except ImportError:
    def colored(str, col):
        return str
