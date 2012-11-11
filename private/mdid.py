#!/usr/bin/env python3

mdchars='23456789abcdefghjkmnpqstuvwxyz'

def md2int(md):
    if isinstance(md, int):
        return md
    md=str(md)
    if md.startswith('md'):
        md=md[2:]
    res=0
    for i in md:
        if i not in mdchars:
            raise ValueError('invalid id: %s' % repr(md))
        res*=len(mdchars)
        res+=mdchars.find(i)+1
    return res

def int2md(no):
    if not isinstance(no, int):
        no=str(no)
        if not no.startswith('md'):
            no='md'+no
        for i in no[2:]:
            if i not in mdchars:
                raise ValueError('invalid id: %s' % repr(md))
        return no
    if no<=0:
        raise ValueError('invalid id: %s' % repr(no))
    res=''
    while no>0:
        no, reminder=divmod(no-1, len(mdchars))
        res=mdchars[reminder]+res
    return 'md'+res

