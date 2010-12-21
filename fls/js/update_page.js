function update_page(){
    $.ajax({
        type: "GET",
        url: window.location,
        dataType: "html",
        success: function(data){
            var results = $(data).filter("#results").html();
            if($(results).filter('.entries').text() == "\n        "){
                results = "Nothing to display...";
            }
            $("#results").html(results);
            /* Give a visual que that we updated the page..  */
            $('#auto_update_label').effect("pulsate", { times:3 }, 1000);
        },error: function(XMLHttpRequest, textStatus, errorThrown){
            //console.log( "Auto update failed: " + textStatus);
        }
    });
};

function setup_auto_update_page(seconds){
    var auto_update = get_url_arg("autoupdate");
    if(auto_update){
        setInterval("update_page()", seconds*1000);
    }
};
