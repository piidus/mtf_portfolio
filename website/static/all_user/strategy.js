
function hideOrShowDiv(divId) {
  const div = document.getElementById(divId);

  if (div.style.display === 'none') {
    div.style.display = 'block';
  } else {
    div.style.display = 'none';
  }
}

function expiryfetch(data){
  
  console.log(data.nifty.length)
  var numbers = data.nifty
  for (let i = 0; i < numbers.length; i++) {
    console.log(numbers[i]);
  }
  // for 
}
  