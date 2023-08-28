Frab-Based Into- and Outro-Generator
===========================================

This is a scripted pre-, postroll and pause-clip generator. It takes a Frab/frab schedule-xml and artwork as svg and generates .dv- or .ts-clips ready-to-use with the [VOC](https://c3voc.de/)-CRS (Conference Recording System) or any other System. It can aĺso be modified to generate Lossless h264 or something different if reqired.

Following the requirements of the CRS-Setup it generates one postroll, one pause-sequence and multiple prerolls - one per Talk in your Schedule-xml, but it should be simple to modify this if your Setup needs it.

Yes! That's what I want!
------------------------
Okay, let's go.

 - Install python3, python3-lxml, python3-cssutils, python3-wand (or use virtualenv, see below), inkscape and libav-tools
 - Fork this repo on github and clone your personal fork to your local system.
 - Copy one of the existing setup: 00_example_render_byid
    - If you are using a newer version of intro-outro-generator, don't copy any of the other projects, as the __init.py__ may not contain all mandatory parameters in the tasks function.
 - Open `artwork/intro.svg` (preroll template) in inkscape and modify it. You can also just create a new one. For the VOC-Setup you should use a Pixel-Resolution of `1920×1080` (or for the legacy SD/.dv-Pipeline `1024×576`).
 - Group things together that should be animated together (like subtitle and speaker-text)
 - Use Flow-Text (in Inkscape drag an Area of Text instead of just placing a single line). This way the text will automatically wrap inside the specified area if it gets too long.
 - Type Placeholder-Texts where the script should substitute content from your schedule.xml. By default the following placeholders are substituted
   - `$id` - Talk-ID (useful in links to the Frab-Page)
   - `$title` - Title of the Talk
   - `$subtitle` - You guessed it...
   - `$personnames` - Comma-Separated list of Speaker-Names
 - Give IDs to the Objects and Groups you want to animate (Inkscape Shift-Ctrl-O)
 - Edit your copy of __init__.py - this is your project configuration
   - set `scheduleUrl` to the url of your schedule.xml-file
   - modify introFrames (preroll) - see section about the frame-generators below
   - search for `def debug()` and comment the sections about outro (postroll) and pause
   - run `./make.py yourproject/ --debug` to generate your first intro
   - if it looks good, duplicate intro.svg to outro.svg (postroll) and pause.svg (pause-loop) and modify them according to your needs. You can use different IDs in your SVG if required
   - modify outroFrames and pauseFrames like before an test them using `./make.py yourproject/ --debug`
   - if everything look like you'd want them to, run `./make.py yourproject/`.
   - You can use any debianesque linux (can be headless) to generate the videos. More cores help more.
 - Run `./make-snapshots.sh yourproject/` to generate a png from a specific time-index of your .ts or .dv-files. You can run `./make-snapshots.sh yourproject/ 5` to get a png for the frame at the 5th second of all your clips. Default is 3 seconds.
   - Viewing through those pngs to check if all intros are looking good with the real-world titles- and person-names
   - Viewing through the pngs is faster then opening each clip and waiting 5 seconds.

#### Python3 virtualenv

Create virtualenv and fetch python deps:

```
$ virtualenv -p python3 env  
$ . ./env/bin/activate
$ pip3 install -r requirements.txt
```

##### Debian

On debian you need to install ImageMagick and Python lxml dependencies:

```
sudo apt-get install python3-pil libmagickwand-dev libmagickcore5-extra libxml2-dev libxslt1-dev
```

Quick start
--------------------

Start your own project by copying "00_example_render_byid" folder which contains all changes to use the new features.

Just type `./make.py` or `./make.py -h` in the main directory and you'll get the following help information.

```
usage: see help with option -h

C3VOC Intro-Outro-Generator

positional arguments:

  yourproject/
    Path to your project is a required argument.
    Usage: ./make.py yourproject/
    Without any further argument(s) given, your whole project will be rendered.
                            

optional arguments:

  -h, --help

    show this help message and exit

  --debug

    Run script in debug mode and just render the debug values
    given in your projects __init.py__
    This argument must not be used together with --id
    Usage: ./make.py yourproject/ --debug
                            
  --id ID [ID ...]

    Only render the given ID(s) from your projects schedule.
    This argument must not be used together with --debug
    Usage: ./make.py yourproject/ --id 4711 0815 4223 1337
    To skip all IDs (just generate intro/outro/background files) use it with --id 000000
                            
  --skip SKIP [SKIP ...]

    Skip outro, pause and/or background files in rendering if not needed.
    This argument must not be used together with --debug
    Usage: ./make.py yourproject/ --skip pause out bg
    Example - only generate outro: ./make.py yourproject/ --skip pause bg
    Example - only generate pause and background: ./make.py yourproject/ --skip out
```

The Frame-Generators
--------------------
The animation sequence is controlled by the three frame-generator routines vorspanFrames, abspannFrames and pauseFrames. Each of them yields one tupel per frame. This Frame-Tupel contains one Sub-Tupel per Animated Element, which has one of two forms:

### CSS-Style-Modifications
`('logo',  'style',    'opacity', 1),` - locate object with id `logo` in the svg, parse its `style`-attribute as css-inline-string and change the value of the css-property `opacity` to 1. The Tupel-Element `'style'` is fixed and declares the type of action which is applied to the specified element. All other tupel-mebers can be modified to suit your needs.

To form an fade-in-opacity-animation, the frame-generator could look like this:

	# three seconds of animation
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

`easeInCubic` is an easing-function stolen from the [jquery-easing plugin](http://gsgd.co.uk/sandbox/jquery/easing/jquery.easing.1.3.js) ([easing-cheat-sheet](http://easings.net/)). They take 4 parameters:
 - t: current time
 - b: beginning value
 - c: change In value
 - d: duration (of time)

So to fade the logo out, the generator yould look like this:

	# three seconds of animation
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 1, -1, frames)),
		)

By yielding multiple sub-tuples, you can animate multiple elements at the same time using different easings. Its up to you to find a combination that looks nice with your artwork.

### XML-Attribute-Modifications
The other form a sub-tuble can have is `('box',   'attr',     'transform', 'translate(0,0)')` - locate object with id `box` in the svg, and set its `transform`-attribute to `translate(0,0)`. This can be used to animate things not specifiable by css - like the spacial translation of an object. A suitable generator, that animates the element `box` in an upward movement, could look like this:

	# three seconds of animation
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('box',   'attr',     'transform', 'translate(0,%.4f)' % easeOutQuad(i, 100, -100, frames) ),
		)

FEM/VOC-Tracker-Integration
---------------------------
*that script-Z-thingy*
The [FEM](http://fem.tu-ilmenau.de/) and the [VOC](https://c3voc.de/) uses a special Ticket-Tracker to keep track of the Talks on an event. Various tasks are performed around the recorded Videomaterial (preparing, cutting, encoding, releasing) - synchronized by the Tracker. The files starting with `script-Z` are experiments to integrate the intro-rendering into this process. On some Events the Schedule is very fluid with talks being addes or names changing over the whole conference. Using the Scripts to render the prerols when they are actually needed (and not some days before the conference) would help to get the always-freshest prerolls but it would an additional (computational intense) task to the publishing process.

Generating an Live-Stream-Overlay
---------------------------------
While your working on your Video-Artwork you can create another required asset: the stream overlay. When we'll live-stream your Talks we can't send prerolls ovet the live-stream. To let your viewer now what program they are watching at, we usually overlay a transparent image over the live-stream like most television programs do, too.
Just create another SVG of the size 1920×1080 (or 1024×576 if you're only targeting the legacy SD-Pipeline) and throw your logo into your prefered corner. To have it looking good we would suggest
 - to test it on dark as well as bright background and add a glow or a backround-box if neccessary
 - avoid thin lines or small text that will not be visible in the final size
 - set an opacity of 0.8 to 1.0 (below 0.8 it usually won't be recognizable on a bumpy background)
Save your file as `artwork/overlay.svg`

When you're done, call `./make-overlay.sh yourproject/` which will generate three .pngs in your artwork directory. One of them looks squeezed - don't worry, that is correct.

It works! It doesn't work!
--------------------------
If it works, push your code to github. This way everybody can see which beautiful animations you created and we can all learn from each other.
If it doesn't work, ask [on IRC](https://kthx.de:9090/?channels=voc) or on [the Mailinglist](mailto:video@lists.ccc.de) and we'll see that we can solve your problem.
If you think you found a bug, [file an Issue](https://github.com/voc/intro-outro-generator/issues). Or even better, fix it and [send a Pull-Request](https://github.com/voc/intro-outro-generator/pulls).
