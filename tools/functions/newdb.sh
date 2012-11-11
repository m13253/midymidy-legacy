#!/bin/sh

if [ "$1" ]
then
    set -e
    echo -n "Creating $1..."
    rm -f "$1.new"
    cat | sqlite3 "$1.new"
    chmod 666 "$1.new"
    mv "$1.new" "$1"
    echo -e '\tOK.'
else
    echo 'This is a databace creation tool, it is called by createdb.sh.'
    echo 'Do not execute it manually.'
    echo
fi
