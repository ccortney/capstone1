import re
import requests

api_url = "http://www.boredapi.com/api/activity?"

class ApiCall:

    # calls the api and returns a random activity
    def get_random_activity():
        return requests.get(api_url).json()
    
    # calls the api and returns activity given the activity key
    def get_activity_from_key(key):
        return requests.get(f"{api_url}key={key}").json()

    # calls the api and returns an activity, if possible, for the given parameters
    def get_activity_search(type, price, participants):
        return requests.get(f"{api_url}type={type}&{price}&participants={participants}").json()