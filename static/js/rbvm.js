var nav = {
    '/' : function( event ) {
        console.log("Gone to root");
    },
    
    '/vms' : function( event ) {
        console.log("Gone to vms");
    }
}

$(document).ready(function() {
    
    $.rpc('get_user_details', {
        success : function( data ) {
            $('#login_area').html(data.username);
        }
    });
    
    $.address.change( function ( event ) {
        if (nav.has_key(event.path)) {
            nav[event.path](event);
        } else {
            // 404, do something useful
        }
    });
});
