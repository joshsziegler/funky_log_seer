function (key, values, rereduce) {
    /* Only return unique hosts*/
    var o = {}; 
    var i;
    var len = values.length;
    var to_return = [];
    for(i = 0; i < len; i++){
        o[values[i]] = values[i];
    }
    for(i in o){
        to_return.push(o[i]);
    }
    return to_return;

}
