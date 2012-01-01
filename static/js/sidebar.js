(function( $ ) {
    var sidePanel = $('<div id="sidebar"></div>');
    sidePanel.append($('<h3><a href="#">Virtual Machines</a></h3>'));
    sidePanel.append($('<div>VM list goes here</div>'));
    sidePanel.append($('<h3><a href="#">Options</a></h3>'));
    sidePanel.append($('<div>Settings go here</div>'));
    
    
    $('body').append(sidePanel);
    sidePanel.accordion();
})( jQuery );
