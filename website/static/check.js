// var socket = io();  //'http://localhost:3000'
var socket = io.connect('http://' + document.domain + ':' + location.port + '/my_namespace');
    
    socket.on('custom_event', function (data) {
        console.log(data);
    });
socket.on('connect', function(data) {
    console.log('Connected to the Socket.IO server');
    // console.log(data.data)
    let v = 'I am logging';
    // Send the current date to the server when the client connects
    var currentDate = new Date();
    socket.emit('send_date', { date: currentDate });
    
});
// socket.on('from_js')


socket.on('custom_event', function(data) {
    // alert('it started');
    
    // document.getElementById('message').textContent = data.message;
    console.log('it start')
    console.log(data)
});

socket.on('user_info', function(data){console.log(data)})

socket.on('disconnect', function() {
    console.log('Disconnected from the Socket.IO server');
});

socket.on('server_event', function(data) {
    console.log('Received message: ' + data.data);
});
