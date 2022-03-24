// const { Chart } = require("chart.js");

const $doughnutChart = $("#doughnut-chart");

// Get data: category counts
async function get_category_counts(){
    const res = await axios.get(`http://127.0.0.1:5000/activitycounts`);
    
    // update activityCounts with data
    let activityCounts = [
        res.data['education_count'], 
        res.data['recreational_count'], 
        res.data['social_count'], 
        res.data['diy_count'], 
        res.data['charity_count'], 
        res.data['cooking_count'], 
        res.data['relaxation_count'], 
        res.data['music_count'], 
        res.data['busywork_count'], 
    ];

    // set data for doughnut chart
  doughnutData = {
    labels: [
      'Education',
      'Recreational',
      'Social', 
      'DIY', 
      'Charity',
      'Cooking',
      'Relaxation',
      'Music',
      'Busywork'
    ],
    datasets: [{
      label: 'Completed Activities by Type',
      data: activityCounts,
      backgroundColor: [
        // random colors
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)', 
        'rgb(100, 99, 132)',
        'rgb(54, 200, 96)',
        'rgb(0, 40, 200)', 
        'rgb(30, 100, 30)',
        'rgb(200, 0, 200)', 
      ],
    }]
  };
};

async function show_charts() {
  // run the function, so that we have an array of data to use
  await get_category_counts();

  // create new doughnut chart for completed activities by type
  const doughnutChart = new Chart($doughnutChart, {
    type: 'doughnut',
    data: doughnutData,
    options: {
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: 'Completed Activities by Type',
        }
      }
    },
  });

}

show_charts();


