#!/bin/sh

for i in "$@"
do
    if [ "$i" ]
    then
        BASENAME="$(basename "$i" .mid)"
        timidity --output-stereo -OwS -Aa -a -C0 --reverb=G --preserve-silence -o "$BASENAME.wav" "$i" && \
        sox -S --norm=-1 "$BASENAME.wav" "$BASENAME-gain.wav" && \
        mv "$BASENAME-gain.wav" "$BASENAME.wav" && \
        ffmpeg -y -i "$BASENAME.wav" -acodec libvorbis -aq 2 "$BASENAME.ogg" && \
        rm "$BASENAME.wav"
    fi
done

