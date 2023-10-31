// check date for last algo
$(document).ready(function() {
    // for api
    var api = $("#api").val();
    console.log('a  : '+api);
    // Get the span tag value
    var spanValue = $("#loginDate").text();
    // Split the span tag value to get the date.
    var dateArray = spanValue.split("Time : ")[0].split(" ");
    // console.log(dateArray);
    var date = dateArray[1];
    // console.log(date);
    // Create a Date object from the split date
    var date = new Date(date);
    var date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
    // console.log(date)
    // Get the current date
    var today = new Date();
    var today = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    // console.log(today)
  
    // Check if the date is previous to today
    if (date < today) {
      // Color the span tag red
      $("#loginDate").css("background-color", "red");
    }else($("#loginDate").css("background-color", 'green'))
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
            method : 'GET',
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
             


        })
        .catch(err => {console.log('error1:: '+err)})
    })
});

