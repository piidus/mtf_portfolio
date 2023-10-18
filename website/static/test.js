const socket = io();

function checkStatus(){
    alert('Test Program Working')
};

socket.on('connect', function() {
    console.log('Connected to server');
    socket.send('User has connected!');
    alert('I am connected');
});

socket.on('response', function(data) {
    console.log(data);
});
