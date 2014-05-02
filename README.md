Frab-Based Pre- and Postroll-Generator
===========================================

This is a scripted pre-, postroll and pause-clip generator. It takes a Frab/frab schedule-xml and artwork as svg and generates .dv-clips ready-to-use with the [VOC](https://c3voc.de/wiki/)-CRS (Continuous Recording System) or any other System. It can aĺso be modified to generate Lossless h264 or something different if reqired.

Following the requirements of the CRS-Setup it generates one postroll, one pause-sequence and multiple prerolls - one per Talk in your Schedule-xml, but it should be simple to modify this if your Setup needs it.

Yes! That's what I want!
------------------------
Okay, let's go.

 - Install python2.7, python-lxml, python-cssutils, inkscape and libav-tools
 - Fork this repo on github and clone your personal fork to your local system.
 - Copy one of the existing setups (I'd suggest sotmeu14 for a start).
 - Open ```artwork/vorspann.svg``` (preroll template) in inkscape and modify it. You can also just create a new one. For the VOC-Setup you should use a Pixel-Resolution of ```1024x576``` (16:9 Aspect Ratio).
 - Group things together that should be animated together (like subtitle and speaker-text)
 - Use Flow-Text (in Inkscape drag an Area of Text instead of just placing a single line). This way the text will automatically wrap inside the specified area if it gets too long.
 - Type Placeholder-Texts where the script should substitute content from your schedule-xml. By default the following placeholders are substituted
   - ```$id``` - Talk-ID (useful in links to the Frab-Page)
   - ```$title``` - Title of the Talk
   - ```$subtitle``` - You guessed it...
   - ```$personnames``` - Comma-Separated list of Speaker-Names
 - Give IDs to the Objects and Groups you want to animate (Inkscape Shift-Ctrl-O)
 - Edit your copy of make.py
   - set ```scheduleUrl``` to the url of your schedule.xml-file
   - modify vorspannFrames (preroll) - see section about the frame-generators below
   - search for ```!!! DEBUG MODE !!!``` and comment the sections about abspann (postroll) and pause
   - run ```./make.py --debug``` to generate your first preroll
   - if it looks good, duplicate vorspann.svg to abspann.svg (postroll) and pause.svg (pause-loop) and modify them according to your needs. You can use different IDs if required
   - modify abspannFrames and pauseFrames like before an test them using ```./make.py --debug```
   - it they look like you'd want them to, run ```make.py```.
   - You can use any debianesque linux (can be headless) to generate the videos. More cores help more.

The Frame-Generators
--------------------
The animation sequence is controlled by the three frame-generator routines vorspanFrames, abspannFrames and pauseFrames. Each of them yields one tupel per frame. This Frame-Tupel contains one Sub-Tupel per Animated Element, which has one of two forms:

### CSS-Style-Modifications
```('logo',  'style',    'opacity', 1),``` - locate object with id ```logo``` in the svg, parse its ```style```-attribute as css-inline-string and change the value of the css-property ```opacity``` to 1. The Tupel-Element ```'style'``` is fixed and declares the type of action which is applied to the specified element. All other tupele-mebers can be modified to suit your needs.

To form an fade-in-opacity-animation, the frame-generator could look like this:

	# three seconds of animation
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('logo',  'style',    'opacity', "%.4f" % easeInCubic(i, 0, 1, frames)),
		)

```easeInCubic``` is an easing-function stolen from the [jquery-easing plugin](http://gsgd.co.uk/sandbox/jquery/easing/jquery.easing.1.3.js) ([easing-cheat-sheet](http://easings.net/)). They take 4 parameters:
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
The other form a sub-tuble can have is ```('box',   'attr',     'transform', 'translate(0,0)')``` - locate object with id ```box``` in the svg, and set its ```transform```-attribute to ```translate(0,0)```. This can be used to animate things not specifiable by css - like the spacial translation of an object. A suitable generator, that animates the element ```box``` in an upward movement, could look like this:

	# three seconds of animation
	frames = 3*fps
	for i in range(0, frames):
		yield (
			('box',   'attr',     'transform', 'translate(0,%.4f)' % easeOutQuad(i, 100, -100, frames) ),
		)


It works! It doesn't work!
--------------------------
If it works, push your code to github. This way everybody can see which beautiful animations you created and we can all learn from each other.
If it doesn't work, ask [on IRC](irc://irc.hackint.org/voc), on [the Mailinglist](video@lists.ccc.de) or drop me a [personal mail](github@mazdermind.de) and we'll see that we can solve your problem.
If you think you found a bug, [file an Issue](https://github.com/MaZderMind/c3voc-toolz/issues). Or even better, fix it and [send a Pull-Request](https://github.com/MaZderMind/c3voc-toolz/pulls).
