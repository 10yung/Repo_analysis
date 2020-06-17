import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_github import PyGithub


class GetStarCountsByRepo:
    reponame = ''

    def __init__(self, reponame):
        self.reponame = reponame

    def get(self):
        g = PyGithub().get_instance()
        repo = g.get_repo(self.reponame)
        return repo.stargazers_count

