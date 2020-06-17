import sys
import os

sys.path.append(os.path.abspath('../driver'))

from py_request import PyRequest


class GetDownloadCounts:
    """
        use repositery owner name and repo name to get github download counts information
    """
    owner = ''
    repoName = ''

    def __init__(self, owner, repoName):
        self.owner = owner
        self.repoName = repoName

    def get(self):
        response = PyRequest().get(f'https://api.github.com/repos/{self.owner}/{self.repoName}/releases')
        return response
