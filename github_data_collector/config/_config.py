import json
import os

class Config:
    config_json_dir = ''
    config_abs_path = ''

    def __init__(self) -> None:
        
        #TODO: get config setting base on environment variable
        self.config_abs_path = os.path.dirname(os.path.abspath(__file__))
        self.config_json_dir = self.config_abs_path + '/config_dev.json'

    def get(self):
        with open(self.config_json_dir, 'r') as myfile:
            data = myfile.read()

        return json.loads(data)

    def get_search_setting(self):
        with open(self.config_json_dir, 'r') as myfile:
            data = myfile.read()

        return json.loads(data)['search_setting']

    def get_mysql(self):
        with open(self.config_json_dir, 'r') as myfile:
            data = myfile.read()

        return json.loads(data)['mysql']