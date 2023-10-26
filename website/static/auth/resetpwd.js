// Check email
function sendEmail(){
    var mail = $("#email").val();
    alert("Auth Code Send to :"+ mail);
    // console.log(mail)
    $.ajax({
        type: 'POST',
        url: '/check_email',
        contentType: 'application/json',
        data: JSON.stringify({'email': mail}),
        success: function (data) {
            if (data.exists) {
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
            } else {
                // alert(mail);
                
                alert('Email exists.');
            }
        }
    });

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