#!/bin/bash
if ! pushd $1 >/dev/null 2>&1; then
	echo "call with a project-name, eg. './make-snapshots sotmeu14' after you rendered your dv/ts-files."
	exit 1
fi

ss=$2
if [ -z $ss ]; then
	# three seconds
	ss=3
fi

for dv in *.dv; do
	png="$dv.png"
	echo "$dv @ second $ss -> $png"
	ffmpeg -loglevel error -i $dv -ss $ss -frames:v 1 -vf scale='iw*sar:ih' -f image2 -y -c png $png;
done

for ts in *.ts; do
        png="$ts.png"
        echo "$ts @ second $ss -> $png"
        ffmpeg -loglevel error -i $ts -ss $ss -frames:v 1 -vf scale='iw*sar:ih' -f image2 -y -c png $png;
done

popd >/dev/null 2>&1

