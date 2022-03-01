const $randomActivityHome = $("#random-home");


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

async function get_random() {
    const activityData = await axios.get(`http://127.0.0.1:5000/random`);
    console.log(activityData);
    let activity = $(generateActivity(activityData.data));
    $randomActivityHome.empty();
    $randomActivityHome.append(activity);
}

if (window.location.href == 'http://127.0.0.1:5000/') {
    get_random();
    setInterval(get_random, 5000);
}
