import requests

api_url = "http://www.boredapi.com/api/activity?"

class ApiCall:

    # calls the api and returns a random activity
    @classmethod
    def get_random_activity(cls):
        return requests.get(api_url).json()
    
    # calls the api and returns activity given the activity key
    @classmethod
    def get_activity_from_key(cls, key):
        return requests.get(f"{api_url}key={key}").json()

    # calls the api and returns an activity, if possible, for the given parameters
    @classmethod
    def get_activity_search(cls, type, price, participants):
        return requests.get(f"{api_url}type={type}&{price}&participants={participants}").json()
