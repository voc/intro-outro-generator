Intro- and Outro-Generator for Adobe After Effects 
==================================================

This version of the intro-outro-generator is made to work on Adobe After Effects Files.
It will use your AE project file, use data from your schedule.xml, and renders the project into .ts intro files.

Yes! That's what I want!
------------------------
Okay, let's go.

 - Install Adobe After Effects 2025
 - Install python3, python3-lxml, python3-cssutils (or use virtualenv, see below), inkscape and libav-tools
 - Fork this repo on github and clone your personal fork to your local system.
 - Copy one of the existing setup: voc_ae
 - Open `intro.aepx` and modify it. You can also create a new project. For the VOC-Setup you should use a Pixel-Resolution of `1920×1080` (or for the legacy SD/.dv-Pipeline `1024×576`).
   - If you create a new project, name it `intro.aepx` and also copy `intro.jsx` into the same folder.
   - Create a new composition and name it `intro`.
 - Use Paragraph Text Layers. This way the text will automatically wrap inside the specified area if it gets too long.
 - Type Placeholder-Texts where the script should substitute content from your schedule.xml. By default the following placeholders are substituted
   - `$id` - Talk-ID (useful in links to the Frab-Page)
   - `$title` - Title of the Talk
   - `$subtitle` - You guessed it...
   - `$personnames` - Comma-Separated list of Speaker-Names
 - Rename the Text layers as per their placeholder
   - `intro_id` for the `$id` placeholder
   - `intro_title` for the `$title` placeholder
   - `intro_subtitle` for the `$subtitle` placeholder
   - `intro_personnames` for the `$personnames` placeholder
 - Edit `intro.jsx` and duplicate the required blocks
   - Change the id of the `app.project.item(2)` to the id of your intro composition. (That is the order at which it is showing in the project library)
   - The template included with this repo only replaces `intro_title` and `intro_personnames`
     - Just copy/paste the 2x blocks required, and change the variables, to also use it for the other placeholders.
 - Run `./make-adobe-after-effects.py yourproject/ --debug` to generate your first intro
   - if everything look like you'd want them to, run `./make-adobe-after-effects.py yourproject/ {schedule} `.

#### Python3 virtualenv

Create virtualenv and fetch python deps:

```
$ python3 -m venv env  
$ . ./env/bin/activate
$ pip3 install -r requirements.txt
```

##### Debian

On debian, for python lxml dependencies:

```
sudo apt-get install libxml2-dev libxslt1-dev
```

Quick start
--------------------

Start your own project by copying "voc_ae" folder.

Just type `./make-adobe-after-effects.py` or `./make-adobe-after-effects.py -h` in the main directory and you'll get the following help information.

```
usage: ./make-adobe-after-effects.py yourproject/ https://url/to/schedule.xml

C3VOC Intro-Outro-Generator - Variant to use with Adobe After Effects Files

positional arguments:
  Project folder
                              Path to your project folder with After Effects Files (intro.aep/scpt/jsx)

  Schedule-URL
                              URL or Path to your schedule.xml


optional arguments:
  -h, --help          show this help message and exit
  --debug
                              Run script in debug mode and render with placeholder texts,
                              not parsing or accessing a schedule. Schedule-URL can be left blank when
                              used with --debug
                              This argument must not be used together with --id
                              Usage: ./make-adobe-after-effects.py yourproject/ --debug

  --id IDS [IDS ...]
                              Only render the given ID(s) from your projects schedule.
                              This argument must not be used together with --debug
                              Usage: ./make-adobe-after-effects.py yourproject/ --id 4711 0815 4223 1337
```

How does it work
--------------------
There are two files required to make the render work `intro.aep`, `intro.jsx`. 
`make-adobe-after-effects.py` will run `intro.aepx` with `intro.jsx` as argument.
Once done, the project file will be passed to aerender to create an intermediate <id>.mov file. Make sure you set .mov as a default in After Effects.
Final step is to convert the <id>.mov to <id>.ts
Here are some details about the files and what they are for.

### intro.aepx
This is the After Effects project file. It has to have the following items included:
 - Composition named `intro`
 - Paragraph text layers named `intro_<placeholder>` for each of the supported placeholder

### intro.jsx
This is an After Effects Script file doing the text replacement of the placeholder texts.

````
app.open(new File("$filename"));
var comp;
for (var i = 1; i <= app.project.numItems; i ++) {
    if ((app.project.item(i) instanceof CompItem) && (app.project.item(i).name === 'intro')) {
        comp = app.project.item(i);
        break;
    }
}
var layer_title = comp.layer('intro_title');
var textProp_title = layer_title.property("Source Text");
var textDocument_title = textProp_title.value;

var layer_persons = comp.layer('intro_personnames');
var textProp_persons = layer_persons.property("Source Text");
var textDocument_persons = textProp_persons.value;

textDocument_title.text = "$title";
textProp_title.setValue(textDocument_title);

textDocument_persons.text = "$personnames";
textProp_persons.setValue(textDocument_persons);

app.project.close(CloseOptions.SAVE_CHANGES);
````

To add an additional block to replace another placeholder, copy the following:

````
var layer_<placeholder> = comp.layer('intro_<placeholder>');
var textProp_<placeholder> = layer_<placeholder>.property("Source Text");
var textDocument_<placeholder> = textProp_<placeholder>.value;
textDocument_<placeholder>.text = "$<placeholder>";
textProp_<placeholder>.setValue(textDocument_<placeholder>);
````

Make sure that the correct layer has been added to the AE project file, otherwise the script will fail.

It works! It doesn't work!
--------------------------
If it works, push your code to github. This way everybody can see which beautiful animations you created and we can all learn from each other.
If it doesn't work, ask [on IRC](https://kthx.de:9090/?channels=voc) or on [the Mailinglist](mailto:video@lists.ccc.de) and we'll see that we can solve your problem.
If you think you found a bug, [file an Issue](https://github.com/voc/intro-outro-generator/issues). Or even better, fix it and [send a Pull-Request](https://github.com/voc/intro-outro-generator/pulls).
