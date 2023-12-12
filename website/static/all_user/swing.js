// alert('hi')
const startButton = document.getElementById('startButton');
const shareStatus = document.getElementById('shareStatus');

if (shareStatus.textContent === 'due'){
    startButton.style.display = "none";
}
function startSheare(){    
    alert('Button ')
    // startButton.setAttribute("disabled", "");
    startButton.style.display = "none";

}