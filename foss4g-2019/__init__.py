#!/usr/bin/python3

import subprocess
import os.path
from renderlib import *
from schedulelib import *
from easing import *
import svg.path

# URL to Schedule-XML
scheduleUrl = 'https://talks.2019.foss4g.org/bucharest/schedule/export/schedule.xml'

# For (really) too long titles
titlemap = {
        198: 'Revamp of CRS management in the OSGeo C/C++ stack with PROJ and GDAL',
        398: 'Visualizing Temporal Trends in a Time Series of Satellite Imagery',
        287: 'Linking geospatial foss technologies on big data in biodiversity research',
        273: 'OGC Overview',
        189: '3.6 million points to polygons',
        66: "Creating Wallonia's new very high resolution land cover maps",
        87: 'Automated GIS-based Complex Developed for the Long-term monitoring',
        78: 'UN Open GIS: Spiral 3 Geo-Analysis',
        103: 'Soil Erosion Model Entering Open Source Era with GPU-based Parallelization',
        85: 'A use case of sharing software and experience from all over the world',
        445: 'National Forest Inventory in the Czech Republic presented in Graphs and Maps',
        457: 'GEO 101 - an intro to the Group on Earth Observations (GEO).',
        384: 'The shift of trade powers',
        90: 'Inter-comparison of the Global Land Cover Maps in Africa',
        70: 'Modelling Spatial Accessibility of Primary Health Care in Malawi',
        65: 'A Scalable Approach for Spatio-Temporal Assessment of Photovoltaic',
        313: 'GNOSIS Map Tiles',
        102: 'Comparing INSPIRE and OpenStreetMap data',
        345: 'Exploring large amounts of weather forecast data through FOSS',
        313: 'GNOSIS Map Tiles',
        513: 'EO Data Challenge proposals',
        63: 'Fine spatial scale modelling of Trentino past forest landscape',
        362: 'QGIS as a reference project to find sustainable ways to rock!',
        86: 'Fast insight about the severity of hurricane impact with spatial analysis of Twitter',
        46: 'A FOSS mapping system for support of electronic communication regulations',
        439: 'Using open & closed source s/w to manage Transportation Networks',
        60: 'An open risk index with learning indicators from OSM-tags',
        68: 'Open Science, Knowledge Sharing and Reproducibility as Drivers',
        426: "How to host and access STAC Imagery",
        94: 'Human Geography with Open GIS in Higher Education Course',
        72: 'An open drought monitoring system for the Deduru Oya basin in Sri Lanka',
        396: 'The case of PULSE',
        157: 'Streaming and rendering the Turin 3D geospatial content',
        180: 'Validation of new OGC standard WFS 3.0 and status update of project',
        211: 'Implementing Earth Observation based Wetland Monitoring Capacity in Africa',
        415: 'Social Dynamics in Urban Context (SoDUCo)',
        199: 'SHOGun, GeoServer & QGIS Integration',
        344: 'Implementing an openEO compliant back-end for processing data cubes',
        129: 'Continental Scale Point Cloud Data Management and Exploitation',
        258: 'Using Cloud Optimised GeoTiffs to Query 24 Billion Pixels In Real-Time',
        172: 'Development of a flood risk monitoring system.',
        30: 'Case Study of Data Collection & Data Sharing',
        316: 'GNOSIS Cartographic Map Style Sheets (CMSS)',
        431: 'Flood Vulnerability Index for coastal communities',
        459: 'Processing and refining European Land use Inventory LUCAS for National Needs',
        518: 'Pivoting to Monetize Mobile Hyperlocal Gamification in the Cloud',
}


def introFrames(args):
    #1 Sec Background
    frames = 1*fps
    for i in range(0,frames):
        yield(
            ('text', 'style', 'opacity', 0),
            ('image1105', 'style', 'opacity', 1),
        )

    #2 Sec FadeIn Text
    frames = 2*fps
    for i in range(0,frames):
        yield(
            ('text', 'style', 'opacity', "%.4f" % easeInCubic(i,0,1,frames)),
            ('image1105', 'style', 'opacity', 1),
        )

    #4 Sec Everything
    frames = 4*fps
    for i in range(0,frames):
        yield(
            ('text', 'style', 'opacity', 1),
            ('image1105', 'style', 'opacity', 1),
        )


def outroFrames(args):
    # 5 Sec everything
    frames = 5*fps
    for i in range(0,frames):
        yield(
            ('layer1', 'style', 'opacity', 1),
            ('layer2', 'style', 'opacity', 1),
        )

def pauseFrames(params):
        # 2 sec Fadein Text1
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                        ('text2', 'style', 'opacity', 0),
                )

    # 2 sec Text1
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', 1),
                        ('text2', 'style', 'opacity', 0),
                )

        # 2 sec Fadeout Text1
        frames = 2*fps
        for i in range(0, frames):
            yield (
                        ('text1', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
                        ('text2', 'style', 'opacity', 0),
                )

        # 2 sec blank
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', 0),
                        ('text2', 'style', 'opacity', 0),
                )

        # 2 sec Fadein Text2
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text2', 'style', 'opacity', "%.4f" % easeOutCubic(i, 0, 1, frames)),
                        ('text1', 'style', 'opacity', 0),
                )


        # 2 sec Text2
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text2', 'style', 'opacity', 1),
                        ('text1', 'style', 'opacity', 0),
                )

        # 2 sec Fadeout Text2
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text2', 'style', 'opacity', "%.4f" % (1-easeOutCubic(i, 0, 1, frames))),
                        ('text1', 'style', 'opacity', 0),
                )

        # 2 sec blank
        frames = 2*fps
        for i in range(0, frames):
                yield (
                        ('text1', 'style', 'opacity', 0),
                        ('text2', 'style', 'opacity', 0),
                )

def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 2404,
            '$title': 'Linux Container im High Performance Computing',
            '$subtitle': 'Vom Wal zur Singularität und weiter',
            '$personnames': 'Holger Gantikow'
        }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if event['room'] not in ('Plenary (National Theatre)', 'Ronda Ballroom', 'Fortuna West', 'Fortuna East', 'Rapsodia Ballroom', 'Opera Room', 'Opereta Room', 'Simfonia','Menuet Room','Hora Room','Coralle Room'):
            print("skipping room %s (%s)" % (event['room'], event['title']))
            continue

        if (event['id'] in idlist or not idlist) and not 'intro' in skiplist:
        # generate a task description and put them into the queue
            queue.put(Rendertask(
                infile = 'intro.svg',
                outfile = str(event['id'])+".ts",
                sequence = introFrames,
                parameters = {
                    '$id': event['id'],
                    '$title': event['title'] if event['id'] not in titlemap else titlemap[event['id']],
                    '$subtitle': event['subtitle'],
                    '$personnames': event['personnames']
                }
            ))

    if not 'outro' in skiplist:
        # place a task for the outro into the queue
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
        ))

    if not 'pause' in skiplist:
        # place a task for the pause into the queue
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
        ))
