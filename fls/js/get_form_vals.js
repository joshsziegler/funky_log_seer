function get_form_vals(){
    var file = get_url_arg("file");
    var regex = get_url_arg("regex");
    var limit = get_url_arg("limit");
    var autoupdate = get_url_arg("autoupdate");
    var toptobottom = get_url_arg("toptobottom");
   
    if(file != ""){
        $('select[name="file"]').val(file);
    }
    if(regex != ""){
        regex = regex.replace(/\+/g, ' ');
        $('input[name="regex"]').val(regex);
    }
    if(limit!= ""){
        $('select[name="limit"]').val(limit);
    }
    if(autoupdate != ""){
        $('input[name="autoupdate"]').attr('checked', true);
    }
    if(toptobottom == "true"){
        $('input[name="toptobottom"]').attr('checked', true);
    }
};
