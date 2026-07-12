# Electromagnetic Field 2026

## What you need

* EMF intro template from kunsis nextcloud
* EMFs version on Raleway wit extra emojis from EMFs infobeamer account
* if you're on MacOS: `brew install ffmpeg-full`

## prepare

```sh
ffmpeg -i emf-intro.m4v -f lavfi -i anullsrc -map 0:v -map 1:a -c:v copy -c:a aac -shortest intro.ts
```

## run

In the root of this repository:

```sh
./make-ffmpeg.py emf2026/ --ffmpeg /opt/homebrew/Cellar/ffmpeg-full/8.1.2/bin/ffmpeg
```
