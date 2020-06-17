import sys
import os
sys.path.append(os.path.abspath('../driver'))

from py_request import PyRequest


class GetCommentCounts:
    """
        use repository owner name and repo name to get comment counts
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
            'comment_count': response[6]['issue']['comments'],
        }



