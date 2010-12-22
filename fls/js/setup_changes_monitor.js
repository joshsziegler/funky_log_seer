function setup_changes_monitor(){
    $('.submit_on_change').change( function(e) {
        /* On changes, resubmit the form */
        $('form.search').submit();
    });
}
