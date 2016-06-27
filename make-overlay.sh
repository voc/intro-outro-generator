#!/bin/bash
if ! pushd "$1/artwork/" >/dev/null 2>&1; then
	echo "call with a project-name, eg. './make-snapshots sotmeu14'"
	exit 1
fi

inkscape --export-width=1920 --export-height=1080 --export-png=overlay-1920x1080.png overlay.svg
inkscape --export-width=1024 --export-height=576 --export-png=overlay-1024x576.png overlay.svg
inkscape --export-width=720  --export-height=576 --export-png=overlay-720x576.png  overlay.svg

popd >/dev/null
