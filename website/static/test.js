const socket = io();

function checkStatus(){
    alert('Test Program Working')
};

socket.on('connect', function() {
    console.log('Connected to server');
    socket.send('User has connected!');
    alert('I am connected');
});

// socket.on('response', function(data) {
//     console.log(data);
// });

function requestNotificationPermission() {
    Notification.requestPermission().then(function(permission) {
        if (permission === 'granted') {
            console.log('Notification permission granted.');
        } else {
            console.log('Notification permission denied.');
        }
    });
}

socket.om('even', function(num){console.log(num)});

socket.on('random_number', function(num) {
    console.log('Received random number:', num);
    showNotification('Random Number', `Generated number: ${num}`);
});

function showNotification(title, message) {
    if (Notification.permission === 'granted') {
        var options = {
            body: message
        };
        var notification = new Notification(title, options);
    }
}