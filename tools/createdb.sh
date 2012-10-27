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
    id   TEXT UNIQUE,
    nick TEXT
);
INSERT INTO users (no, id, nick) VALUES (0, 'root', 'root');
CREATE TABLE music (
    no       INTEGER PRIMARY KEY,
    id       TEXT UNIQUE,
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
    chmod 666 ../data/midymidy.db
    chmod 777 ../data
fi
