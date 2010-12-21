function setup_host_shortcuts(){
    $('.host_key_change').live('click', function(e) {
        e.preventDefault(); 
        $('select[name="file"]').val($(this).text());
        $('form.search').submit();
    });
}
