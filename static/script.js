function add_message(msg){
    var author = msg.substr(0, msg.indexOf(':'))
    var message = msg.substr(msg.indexOf(':')+1)

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
    message_text.appendChild(document.createTextNode(message));
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