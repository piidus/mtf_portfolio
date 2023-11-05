const hideOrShowDiv = document.getElementById("sherStarButton");
const div = document.getElementById("sherStrangleForm");
hideOrShowDiv.addEventListener('click', function () {
  

  if (div.style.display === 'none') {
    div.style.display = 'block';
  } else {
    div.style.display = 'none';
  }
});


function expiryfetch(data) {
  var stockName = $('#stockName').val();
  // console.log(stockName);

  
  // console.log(nifty)
  var secondOption = document.getElementById('expiry')
  if (stockName === 'NIFTY') {
    while (secondOption.options.length > 0){
      secondOption.remove(0)
    }
    for (let i = 0; i < data.nifty.length; i++) {
      var option = document.createElement('option');
      option.value = data.nifty[i];
      option.textContent = data.nifty[i];
      secondOption.appendChild(option);
    }
  } else if(stockName === 'CNXBAN') {
    while (secondOption.options.length > 0){
      secondOption.remove(0)
    }
    for (let i = 0; i < data.bnknifty.length; i++) {
      var option = document.createElement('option');
      option.value = data.bnknifty[i];
      option.textContent = data.bnknifty[i];
      secondOption.appendChild(option);
    }
  };
};