#!/bin/bash
if ! pushd $1 >/dev/null 2>&1; then
	echo "call with a project-name, eg. './make-snapshots sotmeu14' after you rendered your dv-files."
	exit 1
fi

ss=$2
if [ -z $ss ]; then
	# three seconds
	ss=3
fi

for dv in *.dv; do
	png="$(basename $dv .dv).png"
	echo "$dv @ second $ss -> $png"
	avconv -loglevel error -i $dv -ss $ss -frames:v 1 -vf scale='iw*sar:ih' -f image2 -c png $png;
done

popd >/dev/null 2>&1

