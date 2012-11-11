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

    functions/newdb.sh ../data/users.db <<EOM
BEGIN TRANSACTION;
CREATE TABLE users (
    no            INTEGER PRIMARY KEY,
    id            TEXT UNIQUE,
    email         TEXT UNIQUE,
    passwd        BLOB,
    avail         BOOL,
    nick          TEXT,
    bio           TEXT,
    token         BLOB,
    last_seen     REAL,
    sex           INTEGER,
    birth         REAL
);
INSERT INTO users (no, id, avail, nick) VALUES (0, 'root', 0, 'root');
COMMIT;
EOM

    functions/newdb.sh ../data/music.db <<EOM
BEGIN TRANSACTION;
CREATE TABLE music (
    id            INTEGER PRIMARY KEY,
    title         TEXT,
    desc          TEXT,
    filename      TEXT,
    ctime         REAL,
    mtime         REAL,
    atime         REAL,
    uploader      INTEGER,
    category      TEXT,
    tags          TEXT,
    license       TEXT,
    avail         BOOL,
    only_reg      BOOL,
    only_premium  BOOL,
    only_ssl      BOOL,
    accept_region TEXT
);
COMMIT;
EOM

    functions/newdb.sh ../data/comments.db <<EOM
BEGIN TRANSACTION;
CREATE TABLE comments (
    id            INTEGER PRIMARY KEY,
    user          INTEGER,
    music         INTEGER,
    content       TEXT,
    parent        TEXT,
    vote          INTEGER,
    ctime         REAL,
    mtime         REAL,
    avail         BOOL,
    only_reg      BOOL,
    only_premium  BOOL,
    only_ssl      BOOL,
    accept_region TEXT
);
COMMIT;
EOM

    functions/newdb.sh ../data/vote.db <<EOM
BEGIN TRANSACTION;
CREATE TABLE view (
    id            INTEGER PRIMARY KEY,
    view          INTEGER
);
CREATE TABLE score (
    no            INTEGER PRIMARY KEY,
    id            INTEGER,
    score         INTEGER,
    by            INTEGER
);
COMMIT;
EOM

    chmod 777 ../data ../public/midi/pending
    rm -f -v ../public/midi/*.mid ../public/midi/*.ogg ../public/midi/pending/*.mid ../public/midi/pending/*.wav ../public/midi/pending/*.ogg
fi
