(function( $ ) {
    $('body').append($('<div id="sidebar"></div>'));
    $('#sidebar').append($('<h3><a href="#">Virtual Machines</a></h3>'));
    $('#sidebar').append($('<div><ul id="sidebarVms"></ul></div>'));
    $('#sidebar').append($('<h3><a href="#">Options</a></h3>'));
    $('#sidebar').append($('<div><ul id="sidebarSettings"></ul></div>'));
    
    

    $('#sidebar').accordion();
    
    $('#sidebarSettings').append('<li><a href="#/usersettings">User settings</a></li>');
    $('#sidebarSettings').append('<li><a href="#/password">Password change</a></li>');
    
    $('#sidebarVms').append('<li><a href="#/vmlist">VM overview</a></li>');
    $('#sidebar').accordion('destroy').accordion();
    
    
    $.rpc('get_sparse_vm_list', {
        success : function( data ) {
            console.log(data);
        },
        
        error : function ( data ) {
        }
    });
    
})( jQuery );
