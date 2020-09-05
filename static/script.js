function add_message(msg){
    var message = JSON.parse(msg);

    if ('error' in message) {
        var message_div = document.createElement('div');
        message_div.className = 'error_message';
        var message_text = document.createElement('p');
        message_text.className = 'text';

        message_text.appendChild(document.createTextNode(message.error));
        message_div.appendChild(message_text);

        var chat = document.getElementById('chat');
        chat.insertBefore(message_div, chat.firstChild)

        return
    }

    var author = message.author;
    var text = message.text;

    var message_div = document.createElement('div');
    message_div.className = 'message';
    var message_text = document.createElement('p');
    message_text.className = 'text';
    var message_author = document.createElement('span');
    message_author.className = 'author';
    var message_separator = document.createElement('span');
    message_separator.className = 'separator';

    message_separator.appendChild(document.createTextNode(':'))
    message_author.appendChild(document.createTextNode(author))
    message_text.appendChild(message_author);
    message_text.appendChild(message_separator);
    message_text.appendChild(document.createTextNode(text));
    message_div.appendChild(message_text);

    var chat = document.getElementById('chat');
    chat.insertBefore(message_div, chat.firstChild)
}

var socket = io.connect(HOST + ':' + PORT);
socket.on('message', function(msg) {
    add_message(msg)
});

socket.on('connect', function(msg) {
    socket.send('START')
});