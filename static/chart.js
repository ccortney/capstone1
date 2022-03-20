const $lineChart = $("#line-chart");

const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    datasets: [{
      label: 'Testing Chart.js',
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
    }]
  };

const lineChart = new Chart($lineChart, {
    type: 'line',
    data: data,
})
