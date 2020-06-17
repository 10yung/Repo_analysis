import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_request import PyRequest


class GetRepoCommentSummary:
    """
        use repositery owner name and repo name to get github commet information
        {
            "total_count": 5,
            "+1": 3,
            "-1": 1,
            "laugh": 0,
            "confused": 0,
            "heart": 1,
            "hooray": 0,
            "url": "https://api.github.com/repos/octocat/Hello-World/issues/comments/1/reactions"
        }
    """
    owner = ''
    repoName = '' 

    def __init__(self, owner, repoName):
        self.owner = owner
        self.repoName = repoName
    
    def get(self):
        response = PyRequest().get_with_extra_mediatype(f'https://api.github.com/repos/{self.owner}/{self.repoName}/issues/comments')
        return response[-1]['reactions']

