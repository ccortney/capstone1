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

    # def completed_categories(user_id):
    #     results = UserActivity.query.filter(UserActivity.user_id == user_id, 
    #     UserActivity.status == 'completed').all()

    #     education_count = results.query.filter()
    #     recreational_count = 
    #     social_count = 
    #     diy_count = 
    #     charity_count = 
    #     cooking_count = 
    #     relaxation_count = 
    #     music_count = 
    #     busywork_count = 