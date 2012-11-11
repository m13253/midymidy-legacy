#!/usr/bin/env python3

def res2dict(columns, result):
    return dict(zip(columns, result))

def col2select(columns, table=None, conditions=None):
    return 'SELECT '+', '.join(columns)+(' FROM '+table if table else '')+(' '+conditions if conditions else '')+';'

def col2insert(columns, table=None):
    return 'INSERT'+(' INTO '+table if table else '')+' ('+', '.join(columns)+') VALUES ('+', '.join('?'*len(columns))+');';

