function get_url_arg( name ){
    /*  To use this, see the following */
    /* http://www.foo.com/index.html?bob=123&frank=321&tom=213#top */
    /* var name = get_url_arg( 'name' ); */
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( window.location.href );
    if( results == null ){
        return "";
    }else{
        return unescape(results[1]);
    }   
};
