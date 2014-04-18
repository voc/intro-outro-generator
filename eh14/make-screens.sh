#!/bin/bash
mkdir -p screens
for name in ../*.dv; do
	avconv -i $name -ss 3 -frames:v 1 -vf scale='iw*sar:ih' -f image2 -c png screens/$(basename $name .dv).png;
done
