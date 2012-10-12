
function getshebang() {
    var she = location.hash;
    if(!she)
        return undefined;
    var idx = she.indexOf("!");
    if(idx==-1)
        return undefined;
    she = she.substr(idx+1);
    idx = she.indexOf("?");
    if(idx==-1)
        return she;
    else
        return she.substr(0, idx);
}

function getrequest() {
    var req = location.pathname;
    var idx = req.indexOf("?");
    var res = {};
}

function getsheqo() {
    var res = {};
    var she = location.hash;
    var req = location.href;
    var idx = she.lastIndexOf("?");
    if(idx==-1)
        she = "";
    else
        she = she.substr(idx+1);
    var idx = she.indexOf("!");
    if(idx!=-1)
        she = she.substr(0, idx);
    var idx = req.indexOf("?");
    if(idx==-1)
        req = "";
    else
        req = req.substr(idx+1);
    var idx = req.indexOf("#");
    if(idx!=-1)
        req = req.substr(0, idx);
    var idx = req.indexOf("!");
    if(idx!=-1)
        req = req.substr(0, idx);
    she = (req+"&"+she).replace(/\?/g, "&").replace(/\+/g, "%20").split("&");
    for(var i in she) {
        if(!she[i])
            continue;
        var idx = she[i].indexOf("=");
        var key;
        var val;
        if(idx==-1) {
            key = decodeURIComponent(she[i]);
            val = null;
        } else {
            key = decodeURIComponent(she[i].substr(0, idx));
            val = decodeURIComponent(she[i].substr(idx+1));
            if(val.match(/^\-?[0-9]+$/)) {
                var val1 = parseInt(val, 10);
                if(val1==val1) /* not NaN */
                    val = val1;
            } else if(val=="true")
                val = true;
            else if(val=="false")
                val = false;
        }
        if(key.substr(-2, 2)=="[]") {
            key=key.substr(0, key.length-2);
            if(!Array.isArray(res[key]))
               res[key] = new Array();
            res[key].push(val);
        } else
            res[key] = val;
    }
    return res;
}

// https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Array/isArray#Compatibility
if(!Array.isArray) {
    Array.isArray = function (vArg) {
        return Object.prototype.toString.call(vArg)==="[object Array]";
    };
}

