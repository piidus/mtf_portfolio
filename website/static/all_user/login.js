// check date for last algo
$(document).ready(function() {
    // Get the span tag value
    var spanValue = $("#loginDate").text();
    // Split the span tag value to get the date.
    var dateArray = spanValue.split("Time : ")[0].split(" ");
    // console.log(dateArray);
    var date = dateArray[1];
    // console.log(date);
    // Create a Date object from the split date
    var date = new Date(date);
    // console.log(date)
    // Get the current date
    var today = new Date();
  
    // Check if the date is previous to today
    if (date < today) {
      // Color the span tag red
      $("#loginDate").css("background-color", "red");
    }
  });

// Get references to the form and button
const form = document.getElementById('myForm');
const toggleButton = document.getElementById('toggleButton');

 // Add a click event listener to the button
 toggleButton.addEventListener('click', function() {
     // Toggle the visibility of the form
     if (form.classList.contains('hidden-form')) {
         form.classList.remove('hidden-form');
     } else {
         form.classList.add('hidden-form');
     };
});
// create api login url
$(document).ready(function(){
    $('#api_login').on('submit', function(event){
        event.preventDefault();
        var userId = $('#user_id').val();
        var param = 'login_api';
        const request = new Request('/icici_login',{
            method : 'POST',
            headers : {
                'Content-Type': 'application/json',
            },
            body : JSON.stringify({
                param : param,
                user_id : userId,
            })
        });
        
        // fetch start
        fetch(request)
        // .then(response => response.json())
        .then(response => response.json())
        .then(data => {
            var newLink = data['new_link'];
            var newTab = window.open(newLink, '_blank');
             // Attach an event listener to check the URL when the new tab is fully loaded
                // newTab.addEventListener('load', check_url());
                // newTab.addEventListener('laod', checkURL())
                // need Update


        })
        .catch(err => {console.log('error1:: '+err)})
    })
});



function check_url(){
    fetch('/check_url')
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(err => {console.log('err2'+err);
    })
};

    // Function to monitor URL changes
    function checkURL() {
        // Function to log a message in the parent window's console
        function logInParentConsole(message) {
            if (window.opener && window.opener.console) {
                window.opener.console.log(message);
            }
        }
    }