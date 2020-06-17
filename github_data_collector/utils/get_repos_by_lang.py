import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_request import PyRequest

class GetReposByLang:
    """
        use programming language and page and page leng to get repositories
        {
            "q": "language:python", (required)
            "page": 1,
            "per_page": 10 (repo number)
        }
    """
    url_query = {}

    def __init__(self, url_query = None):
        self.url_query = url_query
    
    def get(self):
        response = PyRequest().get_with_detail(f"https://api.github.com/search/repositories?{self.url_query}")

        return {
            "headers" : response['headers'],
            "pagination": response['links'],
            "body" : response['body']['items']
        }