#!/bin/bash

rm -rf thumbs
mkdir thumbs

for intro in *.ts; do
	echo $intro
	ffmpeg -hide_banner -loglevel quiet -ss 4 -i "${intro}" -frames:v 1 "thumbs/${intro}.png"
done
