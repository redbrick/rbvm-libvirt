
/**
 * Default constructor.
 */
function EventBus() {
    this.listeners = {};
    
}

/**
 * Publish an event
 *
 * @param event         The event (a string)
 * @param data          The data parameter to be sent to every callback
 */
EventBus.prototype.publish = function(event, data) {
    if (event in this.listeners) {
        for (index in this.listeners[key]) {
            if (this.listeners[key][index] != null) {
                this.listeners[key][index](data);
            }
        }
    }
}

/**
 * Subscribe to an event.
 *
 * @param event         An event (a string)
 * @param callback      The function to be executed on this event
 * @return              An identifier which can be used to remove this callback
 *                      from this event.
 */
EventBus.prototype.subscribe = function(event, callback) {
    if (!(event in this.listeners)) {
        this.listeners['event'] = [];
    }
    
    this.listeners['event'].push(callback);
    
    return this.listeners['event'].length - 1;
}

/**
 * Unsubscribe from an event.
 *
 * @param event         The event name (a string)
 * @param identifier    The callback identifier (returned by subscribe())
 */
EventBus.prototype.unsubscribe = function (event, identifier) {
    if (!(event in this.listeners)) {
        return;
    }
    
    // Don't pop it, replace it with a nop to preserve other identifiers
    this.listeners['event'][identifier] = function(data) {};
}

var eventBus = new EventBus();
