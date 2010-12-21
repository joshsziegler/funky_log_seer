function setup_search_shortcuts(){
    $('.search_shortcut').live('click', function(e) {
        e.preventDefault();
        $('input[name="regex"]').val($(this).text());
        $('form.search').submit();
    });
}
