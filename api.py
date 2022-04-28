import requests
from models import UserActivity

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

    # returns the count of activities completed for each category
    def completed_categories(user_id):
        results = UserActivity.query.filter(UserActivity.user_id == user_id, 
        UserActivity.status == 'completed').all()

        activity_types = []

        for result in results:
            activity = ApiCall.get_activity_from_key(result.activity_id)
            activity_types.append(activity['type'])
        
        counts = {
            'education_count': len([type for type in activity_types if type == 'education']), 
            'recreational_count': len([type for type in activity_types if type == 'recreational']), 
            'social_count': len([type for type in activity_types if type == 'social']), 
            'diy_count': len([type for type in activity_types if type == 'diy']), 
            'charity_count': len([type for type in activity_types if type == 'charity']), 
            'cooking_count': len([type for type in activity_types if type == 'cooking']), 
            'relaxation_count': len([type for type in activity_types if type == 'relaxation']), 
            'music_count': len([type for type in activity_types if type == 'music']), 
            'busywork_count': len([type for type in activity_types if type == 'busywork']) 
        }
        
        return counts
    

            
