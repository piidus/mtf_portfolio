$(document).ready(function(){
    // check api loin 
    $("#api_login").on('submit', function(event){
        event.preventDefault();
        var data = $("#user_id").val();
        $.ajax({
            type: 'POST',
            url: '/icici_login',
            data: $(this).serialize(),
            success: function(response){
                  
                var newLink = response.new_link;
                // console.log(newLink)
                // Create a new tab with JavaScript
                var newTab = window.open(newLink, '_blank');
                
            }
        });

       
    });
    
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
     }
 });