// Load Expiry Dates
function chooseExpiry(data) {
    let ticker = document.getElementById('ticker').value;
    ticker = ticker.toLowerCase();
    console.log(data[ticker]);
    const selectElement = document.getElementById('expiryDates');
    while (selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }
    const optionsArray = data[ticker];

    for (let option of optionsArray) {
        const optionElement = document.createElement('option');
        optionElement.textContent = option;
        optionElement.value = option
        selectElement.appendChild(optionElement);
    }

}




// // Sample time series data
// let timeSeriesData = {
//     time: ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
//     value: [10, 12, 8, 15, 11, 14, 13]
// };

// // Function to calculate SMA
// function calculateSMA(data, period) {
//     const smaValues = [];
//     for (let i = period - 1; i < data.value.length; i++) {
//         const sum = data.value.slice(i - period + 1, i + 1).reduce((acc, val) => acc + val, 0);
//         const sma = sum / period;
//         smaValues.push(sma);
//     }
//     return smaValues;
// }

// // Choose a period for SMA (e.g., 3)
// let smaPeriod = 3;

// // Calculate initial SMA values
// let smaValues = calculateSMA(timeSeriesData, smaPeriod);

// // Create initial time series trace
// const timeSeriesTrace = {
//     type: 'scatter',
//     mode: 'lines+markers',
//     x: timeSeriesData.time,
//     y: timeSeriesData.value,
//     name: 'Time Series',
//     line: { color: 'blue' }
// };

// // Create initial SMA trace
// const smaTrace = {
//     type: 'scatter',
//     mode: 'lines',
//     x: timeSeriesData.time.slice(smaPeriod - 1),
//     y: smaValues,
//     line: { color: 'red' },
//     legendgroup: 'group1',  // Added legend group
//     showlegend: false  // Hide legend
// };

// // Display initial SMA values on the chart
// const annotations = smaValues.map((sma, index) => ({
//     x: timeSeriesData.time[index + smaPeriod - 1],
//     y: sma,
//     xref: 'x',
//     yref: 'y',
//     text: `SMA: ${sma.toFixed(2)}`,
//     showarrow: true,
//     arrowhead: 4,
//     ax: 0,
//     ay: -40
// }));

// var data = [timeSeriesTrace, smaTrace];

// var layout = {
//     title: 'Time Series with SMA',
//     xaxis: {
//         title: 'Time',
//         range: [timeSeriesData.time[0], timeSeriesData.time[smaPeriod - 1]],
//         type: 'category'
//     },
//     yaxis: { title: 'Value' },
//     annotations: annotations
// };

// Plotly.newPlot('myDiv', data, layout);

// // Simulate updating the chart with new values every 2 seconds
// function updateChart() {
//     // Simulate new data point
//     const newValue = Math.floor(Math.random() * 10) + 10;

//     // Get current time
//     const currentTime = new Date().toLocaleTimeString('en-US', { hour12: false });

//     // Update time series data
//     timeSeriesData.time.push(currentTime);
//     timeSeriesData.value.push(newValue);

//     // Keep only the last 10 data points
//     if (timeSeriesData.time.length > 10) {
//         timeSeriesData.time.shift();
//         timeSeriesData.value.shift();
//     }

//     // Update SMA values
//     smaValues = calculateSMA(timeSeriesData, smaPeriod);

//     // Update traces
//     Plotly.update('myDiv', {
//         x: [timeSeriesData.time, timeSeriesData.time.slice(smaPeriod - 1)],
//         y: [timeSeriesData.value, smaValues],
//         text: [`SMA: ${newValue.toFixed(2)}`]
//     });

//     // Add new SMA values annotations
//     for (let i = 0; i < smaValues.length; i++) {
//         const annotation = {
//             x: timeSeriesData.time[i + smaPeriod - 1],
//             y: smaValues[i],
//             xref: 'x',
//             yref: 'y',
//             text: `SMA: ${smaValues[i].toFixed(2)}`,
//             showarrow: true,
//             arrowhead: 4,
//             ax: 0,
//             ay: -40
//         };
//         Plotly.relayout('myDiv', { annotations: [annotation] }, []);
//     }

//     // Schedule the next update after 2 seconds
//     setTimeout(updateChart, 2000);
// }

// // Start the initial update
// updateChart();
