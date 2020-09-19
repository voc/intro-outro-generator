#!/usr/bin/python3

import easing
import renderlib

# URL to Schedule-XML
scheduleUrl = "https://conf.archlinux.org/schedule2020.xml"


def introFrames(args):
    # fade in logo
    frames = 1 * renderlib.fps
    for i in range(0, frames):
        yield (
            (
                "logo",
                "style",
                "opacity",
                easing.easeInQuad(i, 0, 1, frames),
            ),
            ("conf_title", "style", "opacity", 0),
            ("title", "style", "opacity", 0),
            ("subtitle", "style", "opacity", 0),
            ("persons", "style", "opacity", 0),
            ("id", "style", "opacity", 0),
        )
    # fade in conf_title
    frames = 1 * renderlib.fps
    for i in range(0, frames):
        yield (
            (
                "conf_title",
                "style",
                "opacity",
                easing.easeInQuad(i, 0, 1, frames),
            ),
            ("title", "style", "opacity", 0),
            ("subtitle", "style", "opacity", 0),
            ("persons", "style", "opacity", 0),
            ("id", "style", "opacity", 0),
        )

    # show conf_title and logo for 1 second
    frames = 1 * renderlib.fps
    for i in range(0, frames):
        yield (
            ("logo", "style", "opacity", 1),
            ("conf_title", "style", "opacity", 1),
            ("title", "style", "opacity", 0),
            ("subtitle", "style", "opacity", 0),
            ("persons", "style", "opacity", 0),
            ("id", "style", "opacity", 0),
        )

    # move logo and conf_title to right
    frames = 2 * renderlib.fps
    for i in range(0, frames):
        xshift = (i + 1) * 135 / frames
        yield (
            ("logo", "style", "opacity", 1),
            ("conf_title", "style", "opacity", 1),
            ("title", "style", "opacity", 0),
            ("subtitle", "style", "opacity", 0),
            ("persons", "style", "opacity", 0),
            ("id", "style", "opacity", 0),
            ("logo", "attr", "transform", f"translate({xshift}, 0)"),
            ("conf_title", "attr", "transform", f"translate({xshift}, 0)"),
        )

    # fade in title, subtitle, persons and id
    frames = 2 * renderlib.fps
    for i in range(0, frames):
        yield (
            ("title", "style", "opacity", easing.easeInQuad(i, 0, 1, frames)),
            (
                "subtitle",
                "style",
                "opacity",
                easing.easeInQuad(i, 0, 1, frames),
            ),
            (
                "persons",
                "style",
                "opacity",
                easing.easeInQuad(i, 0, 1, frames),
            ),
            ("id", "style", "opacity", easing.easeInQuad(i, 0, 1, frames)),
            (
                "logo",
                "attr",
                "transform",
                f"translate({xshift}, 0)",
            ),
            (
                "conf_title",
                "attr",
                "transform",
                f"translate({xshift}, 0)",
            ),
        )
    # show whole image for 2 seconds
    frames = 2 * renderlib.fps
    for i in range(0, frames):
        yield (
            ("title", "style", "opacity", 1),
            ("subtitle", "style", "opacity", 1),
            ("persons", "style", "opacity", 1),
            ("id", "style", "opacity", 1),
            (
                "logo",
                "attr",
                "transform",
                f"translate({xshift}, 0)",
            ),
            (
                "conf_title",
                "attr",
                "transform",
                f"translate({xshift}, 0)",
            ),
        )


def backgroundFrames(parameters):
    frames = 20 * renderlib.fps
    for i in range(0, frames):
        xshift = (i + 1) * 300 / frames
        yshift = (i + 1) * (150 / frames)
        yield (
            (
                "logo_pattern",
                "attr",
                "transform",
                "translate(%.4f, %.4f)" % (xshift, yshift),
            ),
        )

    frames = 20 * renderlib.fps
    for i in range(0, frames):
        xshift = 300 - ((i + 1) * (300 / frames))
        yshift = 150 - ((i + 1) * (150 / frames))
        yield (
            (
                "logo_pattern",
                "attr",
                "transform",
                "translate(%.4f, %.4f)" % (xshift, yshift),
            ),
        )


def outroFrames(args):
    # fadein outro graphics
    frames = 3 * renderlib.fps
    for i in range(0, frames):
        yield (
            (
                "logo",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.01, 1, frames),
            ),
            (
                "conf_title",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.01, 1, frames),
            ),
            (
                "c3voclogo",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.01, 1, frames),
            ),
            (
                "c3voctext",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.01, 1, frames),
            ),
            (
                "bysalogo",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.01, 1, frames),
            ),
            (
                "bysatext",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.01, 1, frames),
            ),
        )
    frames = 3 * renderlib.fps
    for i in range(0, frames):
        yield (
            ("logo", "style", "opacity", 1),
            ("conf_title", "style", "opacity", 1),
            ("c3voclogo", "style", "opacity", 1),
            ("c3voctext", "style", "opacity", 1),
            ("bysalogo", "style", "opacity", 1),
            ("bysatext", "style", "opacity", 1),
        )


def pauseFrames(args):
    # fade heartgroups
    frames = int(0.5 * renderlib.fps)
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.25, 0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 1, -0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.25, 0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 1, -0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.25, 0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 1, -0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.25, 0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 1, -0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 0.25, 0.75, frames),
            ),
        )
    for i in range(0, frames):
        yield (
            (
                "group",
                "style",
                "opacity",
                easing.easeInQuad(i, 1, -0.75, frames),
            ),
        )


def debug():
    render(  # noqa
        "intro.svg",
        "../intro.ts",
        introFrames,
        {
            "$id": 7776,
            "$title": "StageWar live!",
            "$subtitle": "Metal Konzert",
            "$persons": "www.stagewar.de",
        },
    )

    render("outro.svg", "../outro.ts", outroFrames)  # noqa

    render("background.svg", "../background.ts", backgroundFrames)  # noqa

    render("pause.svg", "../pause.ts", pauseFrames)  # noqa


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in renderlib.events(scheduleUrl):
        if not (idlist == []):
            if 000000 in idlist:
                print("skipping id (%s [%s])" % (event["title"], event["id"]))
                continue
            if int(event["id"]) not in idlist:
                print("skipping id (%s [%s])" % (event["title"], event["id"]))
                continue

        # generate a task description and put them into the queue
        queue.put(
            renderlib.Rendertask(
                infile="intro.svg",
                outfile=str(event["id"]) + ".ts",
                sequence=introFrames,
                parameters={
                    "$id": event["id"],
                    "$title": event["title"],
                    "$subtitle": event["subtitle"],
                    "$persons": event["personnames"],
                },
            )
        )

    # place a task for the outro into the queue
    if "out" not in skiplist:
        queue.put(
            renderlib.Rendertask(
                infile="outro.svg", outfile="outro.ts", sequence=outroFrames
            )
        )

    # place the pause-sequence into the queue
    if "pause" not in skiplist:
        queue.put(
            renderlib.Rendertask(
                infile="pause.svg", outfile="pause.ts", sequence=pauseFrames
            )
        )

    # place the background-sequence into the queue
    if "bg" not in skiplist:
        queue.put(
            renderlib.Rendertask(
                infile="background.svg",
                outfile="background.ts",
                sequence=backgroundFrames,
            )
        )
