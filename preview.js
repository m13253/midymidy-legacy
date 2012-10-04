
// const
channel_color = [
    "rgba(255,  51,  51, 0.8)", "rgba(102, 102, 255, 0.8)",
    "rgba(255, 255,  51, 0.8)", "rgba(102, 255,  51, 0.8)",
    "rgba(255, 102, 153, 0.8)", "rgba(102,   0, 102, 0.8)",
    "rgba(  0, 204, 255, 0.8)", "rgba(153,  51,  51, 0.8)",
    "rgba( 51,  51,   0, 0.8)", "rgba(  0,   0,   0, 0.8)",
    "rgba(204,  51,   0, 0.8)", "rgba(  0,  51, 102, 0.8)",
    "rgba(255,  51, 204, 0.8)", "rgba(153, 153, 102, 0.8)",
    "rgba(153,   0,   0, 0.8)", "rgba(  0,  51,   0, 0.8)"
];

function getmap(name) {
    try {
        var req = new XMLHttpRequest();
        req.open('GET', name, true);
        req.responseType = "arraybuffer";
        req.onload = function(e) {
            var respBuffer = req.response;
            if(respBuffer) {
                var respBytes = new Uint8Array(respBuffer);
                window.r=respBytes;
                parseBuffer(respBytes, 0);
            }
        }
        req.send();
    } catch(e) {
        reportError(e);
    }
}

function parseBuffer(buf, offset, data) {
    if(!data)
        data = {starttime: new Date(), maxtime: 0, maxheight: 0};
    if(data.mthd==undefined) {
        offset=scanUntil(buf, [0x4d, 0x54, 0x68, 0x64], offset);
        if(offset==-1) {
            reportError("Not a valid MIDI file.");
            return;
        }
        data.mthd={};
        data.mthd.len=scanInt(buf, offset, 4);
        data.mthd.trackType=scanInt(buf, offset+4, 2);
        data.mthd.trackCount=scanInt(buf, offset+6, 2);
        data.mthd.division=scanInt(buf, offset+8, 2);
        offset+=data.mthd.len+4;
        data.tempo={0: data.mthd.division*2};
        data.notes=new Array(256);
        data.notes_time=new Array(256);
        data.notes_vel=new Array(256);
    }

    while(offset!=-1) {
        offset=scanUntil(buf, [0x4d, 0x54, 0x72, 0x6b], offset);
        if(offset==-1)
            break;
        track_end=offset+scanInt(buf, offset, 4)+4;
        offset+=4;
        time=0;
        var meta=null;
        while(offset<track_end && offset!=-1) {
            var tmpoffset=offset;
            delta=scanBigint(buf, offset);
            time+=delta[0];
            offset+=delta[1];
            var meta_=scanInt(buf, offset, 1);
            if((meta_&0x80) || meta==null) {
                meta=meta_
                ++offset;
            }
            if(meta==0xff)
            {
                var cmd=scanInt(buf, offset, 1);
                var metalen=scanInt(buf, offset+1, 1);
                offset+=2;
                switch(cmd) {
                case 0x51:
                    data.tempo[time]=data.mthd.division*1000000/scanInt(buf, offset, metalen);
                    console.log(time+": Tempo="+data.tempo[time]+"delta/s")
                    break;
                }
                offset+=metalen;
            } else {
                var channel=meta&0xf;
                cmd=meta>>4;
                switch(cmd) {
                case 0x9:
                    var note=scanInt(buf, offset, 1)
                    var vel=scanInt(buf, offset+1, 1);
                    offset+=2;
                    noteon(data, delta2sec(data, time), channel, note, vel);
                    break;
                case 0x8:
                    var note=scanInt(buf, offset, 1)
                    var vel=scanInt(buf, offset+1, 1);
                    offset+=2;
                    noteoff(data, delta2sec(data, time), channel, note, vel);
                    break;
                case 0xa:
                case 0xb:
                case 0xe:
                    offset+=2;
                    break;
                case 0xc:
                case 0xd:
                    ++offset;
                    break;
                }
            }
        }
        offset=track_end;
        if(data.maxtime<time)
            data.maxtime=time;
        setTimeout(function() {parseBuffer(buf, offset, data);}, 1); return;
    }
    for(var i in data.notes)
        noteoff(data, data.maxtime, i>>7, i&0x7f, 0);
    var el=document.getElementById("midiloading");
    el.innerHTML="";
    el.style.backgroundColor="lightgray";
    var el=document.createElement("div");
    el.style.position="absolute";
    el.style.top=(data.maxheight+100)+"px";
    el.style.width="1024px";
    el.style.height="100%";
    el.style.zIndex="-1";
    el.style.backgroundColor="lightgray";
    el.style.fontSize="12px"
    el.style.textAlign="right";
    el.innerHTML="MIDI file rendered in "+(new Date()-data.starttime)+"ms."
    document.body.appendChild(el);
}

mintime=null;

function noteon(data, time, channel, note, vel) {
    if(vel==0)
        return noteoff(data, time, channel, note, vel);
    if(mintime==null || mintime>time)
        mintime=time;
    var cn=(channel<<7)|note;
    if(data.notes.indexOf(cn)!=-1)
        noteoff(data, time, channel, note, 0);
    var idx=insArray(data.notes, cn);
    data.notes_time[idx]=time;
}

function noteoff(data, time, channel, note, vel) {
    var idx=data.notes.indexOf((channel<<7)|note);
    if(idx==-1)
        return;
    var el=document.createElement("div");
    el.style.position="absolute";
    var _eltop=data.notes_time[idx]*32;
    el.style.top=_eltop+"px";
    el.style.left=(note*8)+"px";
    if(channel==9)
        el.style.zIndex="1";
    else
        el.style.zIndex="2";
    el.style.width="8px";
    var _elheight=(time-data.notes_time[idx])*32;
    el.style.height=_elheight+"px";
    el.style.backgroundColor=channel_color[channel];
    eldiv=document.getElementById("midiview")
    eldiv.appendChild(el);
    if(data.maxheight<_eltop+_elheight) {
        data.maxheight=_eltop+_elheight;
        eldiv.style.height=data.maxheight+"px";
    }
    delete(data.notes[idx]);
    delete(data.notes_time[idx]);
}

function delta2sec(data, delta) {
    var lastidx=0;
    var total=0;
    for(var i in data) {
        if(i==delta)
            return total;
        else
            return total+(delta-lastidx)/data.tempo[lastidx];
        total+=(i-lastidx)/data.tempo[lastidx];
        lastidx=i;
    }
}

function cmpArray(a, b) {
    if(a.length!=b.length)
        return false;
    else {
        for(var i = 0; i<a.length; ++i)
            if(a[i]!=b[i])
                return false;
        return true;
    }
}

function insArray(arr, v) {
    var i = 0;
    while(true)
        if(arr[++i]==undefined)
        {
            arr[i]=v;
            return i;
        }
}

function scanUntil(arr, dest, from) {
    var arrlen=arr.length;
    var destlen=dest.length;
    var deltalen=arrlen-destlen;
    for(; from<=deltalen; ++from) {
        var i;
        for(i = 0; i<destlen; ++i)
            if(arr[from+i]!=dest[i])
                break;
        if(i==destlen)
            return from+i;
    }
    return -1;
}

function scanInt(arr, from, len) {
    if(len==0)
        return 0;
    var res = 0;
    var hasres = false;
    for(var i = 0; i<len; ++i)
        if(arr[from+i]!=undefined)
        {
            res = (res<<8)|arr[from+i];
            hasres = true;
        }
    if(hasres)
        return res;
}

function scanBigint(arr, from) {
    var res = 0;
    var i = 0;
    while(arr[from+i]!=undefined) {
        res = (res<<7)|(arr[from+i]&0x7f);
        if(arr[from+i]&0x80)
            ++i;
        else
            return [res, i+1];
    }
    return [undefined, i];
}

function reportError(e) {
    document.getElementById("status").innerHTML="Error: "+e;
    console.error(e)
}

// For some buggy browsers that have no Array.indexOf
// https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Array/indexOf#Compatibility
if(!Array.prototype.indexOf)
    Array.prototype.indexOf = function (searchElement /*, fromIndex */ ) {
        "use strict";
        if(this==null)
            throw new TypeError();
        var t = Object(this);
        var len = t.length >>> 0;
        if(len===0)
            return -1;
        var n = 0;
        if(arguments.length>1) {
            n = Number(arguments[1]);
            if (n!=n) // shortcut for verifying if it's NaN
                n = 0;
            else if(n!=0 && n!=Infinity && n!=-Infinity)
                n = (n>0 || -1)*Math.floor(Math.abs(n));
        }
        if(n>=len)
            return -1;
        var k = n >= 0 ? n : Math.max(len - Math.abs(n), 0);
        for(; k<len; k++)
            if(k in t && t[k]===searchElement)
                return k;
        return -1;
    };

// Array Remove - By John Resig (MIT Licensed)
if(!Array.prototype.remove)
    Array.prototype.remove = function(from, to) {
        var rest = this.slice((to || from)+1 || this.length);
        this.length = from<0 ? this.length+from : from;
        return this.push.apply(this, rest);
    };

