// Toggle section
// Get references to the form and button
function hideOrShowDiv(divId) {
    const div = document.getElementById(divId);
  
    if (div.style.display === 'none') {
      div.style.display = 'block';
    } else {
      div.style.display = 'none';
    }
  }
  