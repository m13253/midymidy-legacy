#!/bin/sh

export PATH="$PATH:$PWD/functions"
cd ../public/midi/pending
while true
do
    sleep 2
    for i in `find . -name '*.mid'`
    do
        mid2ogg.sh "$i"
        mv "$i" "`basename "$i" .mid`.ogg" ..
    done
    sleep 3
done
