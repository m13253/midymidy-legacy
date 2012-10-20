#!/bin/bash

set -e
echo 'An empty database will be created.'
echo 'If a database exists, it will be rewritten.'
echo
echo -n 'Are you sure? (Y/n): '
read _answer
echo
if [ -z "$_answer" -o "$_answer" = "y" ]
then
    sqlite3 ../data/midymidy.new.db <<EOM
CREATE TABLE users (
    no   INTEGER PRIMARY KEY,
    id   TEXT,
    nick TEXT
);
INSERT INTO users (no, id, nick) VALUES (0, 'root', 'root');
CREATE TABLE music (
    id       TEXT PRIMARY KEY,
    title    TEXT,
    desc     TEXT,
    filename TEXT,
    time     REAL,
    uploader INTEGER,
    category TEXT,
    tags     TEXT
);
EOM
    mv ../data/midymidy.new.db ../data/midymidy.db
fi
