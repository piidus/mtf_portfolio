// naru alert////////////////////////////////
const naruDiv = document.getElementById("narualert");
naruDiv.addEventListener('click', function () {
  // fetch to acticate
  fetch('/fetch_alert', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
    // body: JSON.stringify({your_variable_key: yourVariable}),
  })
    .then(response => response.json())
    .then(data => {
      // Process the received data and update the DOM
      console.log(data);

});
});

// Option Dates Section /////////////////////////////////////////////
const hideOrShowDiv = document.getElementById("sherStarButton");
const div = document.getElementById("sherStrangleForm");
hideOrShowDiv.addEventListener('click', function () {
  if (div.style.display === 'none') {
    div.style.display = 'block';
  } else {
    div.style.display = 'none';
  }
});


// Fetch expiry and fill the data
function expiryfetch() {
  var stockName = $('#stockName').val();
  // console.log(nifty)
  var secondOption = document.getElementById('expiry');
  while (secondOption.options.length > 0) {
    secondOption.remove(0)
  }
  // Now fetch expiry
  // Fetch data from backend using POST method and pass the variable

  fetch('/fetch_expiry', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
    // body: JSON.stringify({your_variable_key: yourVariable}),
  })
    .then(response => response.json())
    .then(data => {
      // Process the received data and update the DOM
      // console.log(data);
      if (stockName === 'NIFTY') {
        // while (secondOption.options.length > 0){
        //   secondOption.remove(0)
        // }
        for (let i = 0; i < data.nifty.length; i++) {
          var option = document.createElement('option');
          option.value = data.nifty[i];
          option.textContent = data.nifty[i];
          secondOption.appendChild(option);
        }
      } else if (stockName === 'CNXBAN') {
        // while (secondOption.options.length > 0){
        //   secondOption.remove(0)
        // }
        for (let i = 0; i < data.bnknifty.length; i++) {
          var option = document.createElement('option');
          option.value = data.bnknifty[i];
          option.textContent = data.bnknifty[i];
          secondOption.appendChild(option);
        }
      };
      // return data;
    })
    .catch(error => console.error('Error:', error));
};

// console.log(data)
  
  
// };

////////////// 
