function (key, values, rereduce) {
    /* Only return unique hosts*/
    var o = {}; 
    var i;
    var len = values.length;
    var to_return = [];
    if(rereduce == false){
        for(i = 0; i < len; i++){
            o[values[i]] = values[i];
        }
    }else{
        for(i =0; i < len; i++){
            for(y in values[i]){
                o[values[i][y]] = values[i][y];
            }
        }
    }
    for(i in o){
        to_return.push(o[i]);
    }
    return to_return;
}
