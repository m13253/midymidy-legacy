
function getshebang() {
    var she = location.hash;
    if(!she)
        return undefined;
    var idx = she.indexOf('!');
    if(idx==-1)
        return undefined;
    return she.substr(idx+1);
}

