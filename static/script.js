function add_message(msg){
    var message = JSON.parse(msg);
    var message_div = document.createElement('div');
    
    if ('error' in message) {
        message_div.className = 'error_message';
        var text = message.error
        message_div.innerHTML = `<p class='text'>${text}</p>`
    }
    else {
        message_div.className = 'message';
        var author = message.author;
        var text = message.text;
        message_div.innerHTML = `<p class="text"><span class="author">${author}</span><span class="separator">:</span>${text}</p>`
    }

    var chat = document.getElementById('chat');
    chat.insertBefore(message_div, chat.firstChild)
}

var socket = io(HOST + ':' + PORT);
socket.on('message', function(msg) {
    add_message(msg)
});

socket.on('connect', function(msg) {
    socket.send('START')
});