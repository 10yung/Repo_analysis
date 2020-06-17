import sys
import os
sys.path.append(os.path.abspath('../config'))

from _config import Config
from github import Github


class PyGithub:
    conf = {}

    def __init__(self):
        self.conf = Config().get()

    def get_instance(self):
        # using username and password
        g = Github(self.conf['username'], self.conf['password'])

        # or using an access token
        g = Github(self.conf['token'])

        return g