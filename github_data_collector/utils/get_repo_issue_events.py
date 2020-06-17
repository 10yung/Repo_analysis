import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_request import PyRequest


class GetRepoIssueEvents:
    """
        use repositery owner name and repo name to get issue information information
    """
    owner = ''
    repoName = '' 

    def __init__(self, owner, repoName):
        self.owner = owner
        self.repoName = repoName
    
    def get(self):
        response = PyRequest().get(f'https://api.github.com/repos/{self.owner}/{self.repoName}/issues/events')
        #TODO: extract response json with useful data
        return {
            'issue_count': response[6]['issue']['number'],
        }
