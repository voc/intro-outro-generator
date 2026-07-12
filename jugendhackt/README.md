# Jugend Hackt Design

## Usage

With this configuration, intros and an outro can be generated for any Jugend hackt event using the `make-ffmpeg.py` workflow.
The ffmpeg video filter-based workflow uses one background video and applies the title and speaker names on top.

To setup a new event, follow these steps:

1. Generate `outro.ts`: `ffmpeg -loop 1 -i outro.png -f lavfi -i anullsrc -c:v mpeg2video -t 10 -aspect 16:9 -c:a mp2 -b:v 2500k -map 0:v -map 1:a outro.ts`
2. Generate `intro-background.ts`: `ffmpeg -loop 1 -i intro.png -f lavfi -i anullsrc -c:v mpeg2video -t 10 -aspect 16:9 -c:a mp2 -b:v 2500k -map 0:v -map 1:a intro-background.ts`
3. Edit the schedule URL in the `config.ini`
4. Run `./make-ffmpeg.py jugendhackt/` and copy the generated files to the encoder
