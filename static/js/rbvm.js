/**
 * Navigation thingy.
 *
 * When the page URL changes (the bit after the #), one of these
 * is called, depending on the URL. 
 *
 * Each function needs to take an event parameter, which is an
 * object with the following params:
 * .parameters  URL parameters dictionary extracted from the query string (i.e. ?param1=value&param2=value is returned as {'param1':'value', 'param2':'value'})
 * .path        The URL path (/, or /home, or /foo/bar, etc)
 * .pathNames   Path component names ('', or 'home', or 'foo, bar', etc)
 * .queryString The raw query string
 */
var nav = {
    
    '/' : function( event ) {
        console.log("Gone to root");
    },
    
    '/vms' : function( event ) {
        console.log("Gone to vms");
    },
}

/**
 * Initialisation stuff
 */
$(document).ready(function() {
    
    $.rpc('get_user_details', {
        success : function( data ) {
            $('#login_area').html(data.username);
        },
        
        error : function ( error ) {
            window.location.replace("/login");
        }
    });
    
    $.address.change( function ( event ) {
        if (nav[event.path]) {
            nav[event.path](event);
        } else {
            // 404, do something useful
        }
    });
    
    $.getScript('/static/js/sidebar.js');
    $.getScript('/static/js/homepage.js');
});

