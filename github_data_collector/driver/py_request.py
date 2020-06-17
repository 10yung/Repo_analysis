import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from config._config import Config

class PyRequest:
    conf = {}

    def __init__(self):
        self.conf = Config().get()

    def get(self, api_endpoint):
        headers = {'Authorization': 'token ' + self.conf['token']}
        response = requests.get(api_endpoint, headers=headers)
        # print(response.headers)
        return response.json()


    def get_with_detail(self, api_endpoint):
        headers = {'Authorization': 'token ' + self.conf['token']}
        response = requests.get(api_endpoint, headers=headers)
        
        return {
            "headers": response.headers,
            "links": response.links,
            "body": response.json()
        }


    def get_with_extra_mediatype(self, api_endpoint):
        headers = {'Authorization': 'token ' + self.conf['token'], 'Accept': 'application/vnd.github.squirrel-girl-preview'}
        response = requests.get(api_endpoint, headers=headers)

        return response.json()

    def post(self, api_endpoint, payload):
        #TODO: create post action
        print('this is post')