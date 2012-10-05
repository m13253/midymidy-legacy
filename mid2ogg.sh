#!/bin/sh

for i in "$@"
do
  [ -z "$i" ] || (timidity --output-stereo -OwS -Aa -a -C0 --reverb=G -o "$(basename "$i" .mid).wav" "$i" && ffmpeg -y -i "$(basename "$i" .mid).wav" -acodec vorbis -aq 2 -strict -2 "$(basename "$i" .mid).ogg" && rm "$(basename "$i" .mid).wav")
done

