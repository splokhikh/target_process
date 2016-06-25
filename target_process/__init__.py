import json
import colors
from client import TargetProcessClient


class TargetProcess:
    def __init__(self, token):
        self.token = token

        if self.token is None:
            print colors.error("Token cant be empty")
            exit()
        else:
            self.tp = TargetProcessClient(self.token)

    def move_user_stories(self, userStoriesIds, toState):
        if not isinstance(userStoriesIds, list):
            print colors.error("User stories should be list instance")
            exit()

        response = self.tp.get('UserStories', {'id': userStoriesIds})

        if response.status_code != 200:
            print colors.error("Cant get user stories")
            exit()

        userStories = json.loads(response.text)

        if 'Items' not in userStories:
            print colors.error('Bad response')
            exit()

        for userStory in userStories['Items']:
            result = self.tp.post('UserStories', {
                'Id': userStory['Id'],
                'EntityState': {'Id': self.tp.getStateCode(toState)}
            })

            if result.status_code == 200:
                print colors.success("User story {} \"{}\" -> \"{}\"".format(
                    userStory['Id'],
                    userStory['EntityState']['Name'],
                    toState
                ))
            else:
                print colors.error("User story {} update failed".format(id))

