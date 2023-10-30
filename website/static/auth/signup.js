// Check email
function sendEmail(){
    var mail = $("#email").val();
    alert("Auth Code Send to :"+mail)
    const request = new Request('/check_email', {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'email': mail})
    })
    fetch(request)
    .then(response => response.json())
    .then(function (data) {
        console.log(response);
        if (data.exists) {
            alert('Email exists.');
        } else {
            // alert(mail);
            $("#email").prop("disabled" , true);
            $('#hiddenEmail').val(mail); // Set the hidden input value
            $("#sendMailbt").hide();
            var div = document.getElementById("checkCaptcha");
                if (div.style.display === "none") {
                    div.style.display = "block";
                } else {
                    div.style.display = "none";
                }
            $('#recapcha').text(data.code);
        }
    })
    .catch(err => console.log(err))
    

};
function activateSection() {
    var cap = $("#recapcha").text();
    var cap2 = $("#capSec").val();
    // console.log(cap, cap2)
    if (cap === cap2){
        var capSection = document.getElementById("checkCaptcha");
        capSection.style.display = 'none'
        var div = document.getElementById("myDiv");
        if (div.style.display === "none") {
            div.style.display = "block";
        } else {
            div.style.display = "none";
    }}else{alert('Please check the mail')}
};