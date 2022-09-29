# Capstone 1: BoredBoard

An app to help combat boredom. 

## Overview:
Bored? Not sure what to do? BoredBoard allows users to find and filter for activities! With nine activity types (cooking, relaxation, and more!) and 
multiple price and participant ranges, there is an activity for everyone. Users can save activites for later, complete activities now, and will have access to personalized stats on those they save and complete.

## Accessing the App
[https://bored-board.herokuapp.com/ ](https://bored-board.herokuapp.com/ )<br/>
Test Username: testuser    Test Password: password

## Features:
* BoredBoard users join as an individual user and only sees information related to their account. 
* Once logged in, users will see a random activity that they can save or they request a new activity. 
* There is also a filter form that allows users to choose an activity type, price range, and/or number of particpants. 
* Users will see the activities that they have saved (either in progress or completed) along with that activity type. 
* Users will be able to mark an in-progress activity as complete. 
* Users will be able to delete an in-progress or completed activity.
* Users will see the percentage of activities completed, as well as a doughnut chart of completed activites by activity type.

## API:
The activities in BoredBoard are obtained from http://www.boredapi.com. 
The activities from this API are geared more towards older teens and adults. 
Activities are no longer being added to the API, so there is a total of 185 possible activities for users to save and complete. 

## Technology Stack:
This app was created using Python, Flask, SQLAlchemy, Javascript, HTML, and Bootstrap.
