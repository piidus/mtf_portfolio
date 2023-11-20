

///////////////// PIVOT Chart ///////////////////////////

/////////////////////////////////////////////////
// // Sample data (replace this with your actual data)
// const timeSeriesData = {
//     time: ['2023-01-01 09:15', '2023-01-01 09:30', '2023-01-01 09:45', '2023-01-01 10:00', '2023-01-01 10:15', '2023-01-01 10:30', '2023-01-01 10:45', '2023-01-01 11:00', '2023-01-01 11:15', '2023-01-01 11:30', '2023-01-01 11:45', '2023-01-01 12:00', '2023-01-01 12:15', '2023-01-01 12:30', '2023-01-01 12:45', '2023-01-01 13:00', '2023-01-01 13:15', '2023-01-01 13:30', '2023-01-01 13:45', '2023-01-01 14:00', '2023-01-01 14:15', '2023-01-01 14:30', '2023-01-01 14:45', '2023-01-01 15:00', '2023-01-01 15:15'],
//     value: [100, 102, 105, 110, 108, 112, 115, 118, 120, 122, 125, 124, 126, 130, 128, 135, 133, 132, 136, 140, 138, 137, 135, 138, 142, 144, 145]
// };

// // Create traces
// const trace = {
//     x: timeSeriesData.time,
//     y: timeSeriesData.value,
//     type: 'scatter',
//     mode: 'lines'
// };

// // Layout configuration
// const layout = {
//     xaxis: {
//         type: 'date',
//         tickvals: timeSeriesData.time,  // Set tick positions
//         ticktext: timeSeriesData.time.map(time => new Date(time).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})),  // Set tick labels
//         title: 'Time',
//         range: ['2023-01-01 09:15', '2023-01-01 15:15'],
//         tickangle: -45,
//         showline: true,
//         showgrid: true,
//         zeroline: false,
//         linecolor: 'black',
//         linewidth: 2
//     },
//     yaxis: {
//         title: 'Value'
//     }
// };

// // Create the plot
// Plotly.newPlot('myDiv', [trace], layout);





// ////?/////////////////////////////// old code
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
