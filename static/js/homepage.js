(function( $ ) {
    $('#content').remove();
    
    var content = $('<div id="content"></div>');
    content.append($('<b>Main content</b>'));
    $('body').append(content);
    
})(jQuery);
