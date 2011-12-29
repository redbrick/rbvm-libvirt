(function ( $ ) {
    $.rpc = function( name, options ) {
        options.dataType = 'json';
        options.url = '/rpc/' + name;
        
        $.ajax(options);
    };
})( jQuery );