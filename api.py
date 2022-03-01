import requests

api_url = "http://www.boredapi.com/api/activity?"

def get_random_activity():
    return requests.get(api_url).json()