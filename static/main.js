// find the DOM element where random activities will appear on the main homepage
const $randomActivityHome = $("#random-home");

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
        </div>`
}

// call the /random route which will return a random activity
// call the generateActivity function on that activity
// clear the current activity shown on the interface
// Show the new activity
async function get_random() {
    const activityData = await axios.get(`http://127.0.0.1:5000/random`);
    console.log(activityData);
    let activity = $(generateActivity(activityData.data));
    $randomActivityHome.empty();
    $randomActivityHome.append(activity);
}

// when on homepage without logged in user, get random activity. 
// regenerate that random activity every 5 seconds
if (window.location.href == 'http://127.0.0.1:5000/') {
    get_random();
    setInterval(get_random, 5000);
}
