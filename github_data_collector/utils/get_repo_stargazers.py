import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_request import PyRequest


class GetRepoStargazers:
    """
        use repositery owner name and repo name to get github stargazers information
    """
    owner = ''
    repoName = '' 

    def __init__(self, owner, repoName):
        self.owner = owner
        self.repoName = repoName
    
    def get(self):
        response = PyRequest().get(f'https://api.github.com/repos/{self.owner}/{self.repoName}/stargazers')
        return response


