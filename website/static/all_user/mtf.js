
// Get the table body element
const tableBody = document.getElementById("stockTableBody");

function updateStockValues(updatedData){
    // console.log(updatedData)
    for (const symbol in updatedData) {
        const value = updatedData[symbol][0];
        // console.log(symbol)

        // Loop through existing rows to find the corresponding elements
        const rows = tableBody.getElementsByTagName('tr');
        // console.log(rows)
        for (const row of rows) {
            const rowToken = row.dataset.equityShortname;
            // console.log(rowToken)
            if (rowToken === symbol) {
                // Found the corresponding row, update values
                // const shortnameInput = row.dataset.equityShortname;
                const span = row.querySelector('td span');

                span.textContent = value;
                break;  // Stop searching once found
            }
        }
    }
}

// Get all hidden input elements with name "equityToken"
const tokenElements = document.querySelectorAll('input[name="equityToken"]');

// Initialize an array to store the token values
const tokenList = [];

// Iterate through the hidden input elements and add their values to the array
tokenElements.forEach(input => {
    const tokenValue = input.value;
    tokenList.push(tokenValue);
});
// console.log(tokenList)
// console.log(tokenList); //

// Function to make the POST request
function fetchData() {
    // Define the URL for your POST request
    const url = '/mtf_ltp';

    // Define the data to be sent in the request body (if any)
    const data = {
        tokenlist: tokenList,
        
    };

    // Define the request options
    const options = {
        method: 'POST',
        // mode: 'no-cors', // Set mode to 'no-cors'
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    // Make the fetch request
    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            // Process the response data as needed
            // console.log('Response:', data);
            updateStockValues(data);
        })
        .catch(error => {
            // Handle any errors
            console.error('Error:', error);
        });
}

// Call fetchData initially (you can remove this line if you want to start after the first minute)
fetchData();

// Schedule the fetchData function to run every one minute (60,000 milliseconds)
setInterval(fetchData, 30000);