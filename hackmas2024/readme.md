# Hackmas 2024 Readme

Get intro-slate and outro.ts from shared storage or generate from still images by running:
```sh
ffmpeg -loop 1 -i hackmas2024-outro-slate.png -f lavfi -i anullsrc -c:v mpeg2video -t 10 -aspect 16:9 -c:a mp2 -b:v 15000k -map 0:v -map 1:a outro.ts
ffmpeg -loop 1 -i hackmas2024-intro-slate.png -f lavfi -i anullsrc -c:v mpeg2video -t 10 -aspect 16:9 -c:a mp2 -b:v 15000k -map 0:v -map 1:a intro-background.ts
```
