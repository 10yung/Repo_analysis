import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_request import PyRequest



class GetArchivedStatus:

    """
        use repositery owner name and repo name to get issue information information
    """
    owner = ''
    repoName = ''

    def __init__(self, owner, repoName):

        self.owner = owner
        self.repoName = repoName



    def extract_values(self, obj, key):
        """Pull all values of specified key from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        results = extract(obj, arr, key)
        return results

    def get(self):
        response = PyRequest().get(f'https://api.github.com/repos/{self.owner}/{self.repoName}/events')
        #TODO: extract response json with useful data
        return {
                       'archived': self.extract_values(response,'archived')[0]
        }




# new_response = GetSize().get()
# print(new_response)
# result = GetSize().extract_values(new_response, 'has_wiki')
# print(result[0])