# Jugend Hackt Design

Different Jugend hackt events use a similar design for intro and outro, but different accent colors.
This can be achieved by replacing the color and location in a template SVG.

## Usage

With this configuration, intros and an outro can be generated for any Jugend hackt event using the `make-ffmpeg.py` workflow.
The ffmpeg video filter-based workflow uses one background video and applies the title and speaker names on top.

To setup a new event, take the color codes from below and follow these steps:

1. Generate "outro.ts"
  - Copy `outro-template.svg` to `outro.svg`
  - Replace `$LOCATION` in the SVG with the location name (in capital letters)
  - Replace `$alpaca_color` in the SVG with corresponding color code
  - Convert the SVG into png, e.g. with `inkscape --export-filename=outro.png outro.svg`
  - Generate a video from the background: `ffmpeg -loop 1 -i outro.png -f lavfi -i anullsrc -c:v mpeg2video -t 10 -aspect 16:9 -c:a mp2 -b:v 2500k -map 0:v -map 1:a outro.ts`
2. Generate "intro-background.ts"
  - Copy `intro-background-template.svg` to `intro-background.svg`
  - Replace `$LOCATION` in the SVG with the location name (in capital letters)
  - Replace `$alpaca_color` in the SVG with corresponding color code
  - Convert the SVG into png, e.g. with `inkscape --export-filename=intro-background.png intro-background.svg`
  - Generate a video from the background: `ffmpeg -loop 1 -i intro-background.png -f lavfi -i anullsrc -c:v mpeg2video -t 10 -aspect 16:9 -c:a mp2 -b:v 2500k -map 0:v -map 1:a intro-background.ts`
3. Edit the schedule URL in the `config.ini`
4. Run `./make-ffmpeg.py jugendhackt/` and copy the generated files to the encoder

Note: Do **not** commit the customized SVGs to the repo, but keep this folder generic.
If you really want to commit the config, copy this to a different folder.

## Colors

| Location/ Usage              | Color Code | Color Name  |
| ---------------------------- | ---------- | ----------- |
| Jugend hackt Logo            | #00a6de    | Soft Blue   |
| Hamburg, MV                  | #00b48d    | Soft Green  |
| Dresden                      | #f3971b    | Soft Orange |
| Frankfurt                    | #51509d    | Soft Purple |
| Halle                        | #e6414a    | Soft Red    |
| Berlin                       | #00498c    | Deep Blue   |
| AT/Linz                      | #4cad37    | Deep Green  |
| Rhein-Neckar, München, Ulm   | #ea680c    | Deep Orange |
| Köln                         | #4c2582    | Deep Purple |
| CH/Zürich                    | #e52420    | Deep Red    |
| kein Event                   | #e95197    | Pink        |
