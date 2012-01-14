(function( $ ) {
    $('#content').remove();
    
    var content = $('<div id="content"></div>');
    content.append($('<b>Main content</b>'));
    $('body').append(content);
    
    $.rpc('get_vm_list', {
        success : function( data ) {
            console.log(data);
        },
        
        error : function ( data ) {
        }
    });
    
})(jQuery);
