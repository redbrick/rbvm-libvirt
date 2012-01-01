(function( $ ) {
    var sidePanel = $('<div id="sidebar"></div>');
    sidePanel.append($('<h3><b>Virtual Machines</b></h3>'));
    sidePanel.append($('<div id="sidebarVmList">VM list goes here</div>'));
    sidePanel.append($('<h3><b>Options</b></h3>'));
    sidePanel.append($('<div id="sidebarSettings">Settings go here</div>'));
    
    
    $('body').append(sidePanel);
    sidePanel.accordion();
})( jQuery );
