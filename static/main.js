// find the DOM element where random activities will appear on the main homepage
const $randomActivityHome = $("#random-main-home");
const $searchResults = $("#search-results");
const $searchButton = $("#search-btn");
const $randomUserHome = $("#random-home");
const $getRandom = $("#get-random");

get_random();


// Returns the HTML markup for an activity
function generateActivity(activity) {
    return `
        <div id = ${activity.key}>
            <p>
                ${activity.activity}<br>
                Type: ${activity.type}<br>
                Price Rating: ${activity.price}<br>
                Number of Participants: ${activity.participants}<br>
            </p>
            <a href='/activity/${activity.key}/save'>Save</a>
            <button class="get-random">Get Another Activity</button>
        </div>`
}

// call the /random route which will return a random activity
// call the generateActivity function on that activity
// clear the current activity shown on the interface
// Show the new activity
// async function get_random() {
//     const activityData = await axios.get(`http://127.0.0.1:5000/random`);
//     console.log(activityData);
//     let activity = $(generateActivity(activityData.data));
//     $randomActivityHome.empty();
//     $randomActivityHome.append(activity);
// }

async function get_random(){
    const activityData = await axios.get(`http://127.0.0.1:5000/random`);
    console.log(activityData);
    let activity = $(generateActivity(activityData.data));
    $randomUserHome.empty();
    $randomUserHome.append(activity);
}


$("#random-home").on("click", ".get-random", async function(e) {
    e.preventDefault();
    await get_random();
})


// when on homepage without logged in user, get random activity. 
// regenerate that random activity every 5 seconds
// if (window.location.href == 'http://127.0.0.1:5000/') {
//     get_random();
//     setInterval(get_random, 5000);
// }


// async function get_searched_activity() {
//     const activityData = ApiCall.get_activity_search(type, price, participants)
//     console.log(activityData);
//     let activity = $(generateActivity(activityData.data));
//     $searchResults.empty();
//     $searchResults.append(activity);
// }

// async function get_searched_activity(evt) {
//     evt.preventDefault();
//     const activityData = await axios.post(`http://127.0.0.1:5000/search`);
//     console.log(activityData);
//     let activity = $(generateActivity(activityData.data));
//     $searchResults.empty();
//     $searchResults.append(activity);
// }

// $searchButton.on("click", get_searched_activity())

