// const { Chart } = require("chart.js");

const $doughnutChart = $("#doughnut-chart");
  
// naming colors
  let orange = 'FF9B54';
  let yellow = 'FCBA04'; 
  let pink = 'D81159';
  let violet = '6874E8';
  let green = '3BB273';
  let blush = 'FF7B9C';
  let blue = '1E96FC';
  let royal = '072AC8';
  let purple = '54428E'
  
    // [#FF9B54, #FCBA04, #D81159, #6874E8, #3BB273, #FF7B9C, #1E96FC, #072AC8, #54428E]

// Get data: category counts
async function get_category_counts(){
    const res = await axios.get(`${BASE_URL}/activitycounts`);
    
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
      backgroundColor: [`#${orange}`, 
      `#${yellow}`, 
      `#${pink}`, 
      `#${violet}`, 
      `#${green}`, 
      `#${blush}`, 
      `#${blue}`, 
      `#${royal}`, 
      `#${purple}`],
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

$(document).ready(function() {
  if (window.location.pathname == '/home') {
    show_charts();
  }
})



