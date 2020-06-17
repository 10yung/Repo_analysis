import sys
import os
import pandas as pd
import urllib.parse as urlparse

sys.path.append(os.path.abspath('../../config'))
sys.path.append(os.path.abspath('../../utils'))

from _config import Config
from get_repos_by_lang import GetReposByLang
from get_star_counts_by_repo import GetStarCountsByRepo
from get_issue_content_by_repo import GetIssueContent
from pydash import py_
from urllib.parse import unquote


def repos_to_csv(repos_by_lang, page_num):
    repo_issue_content_list = []
    for index, repo in enumerate(repos_by_lang):
        # get repo with basic numerical numerical data
        repos_by_lang[index] = py_.pick(repo, 'full_name', 'forks_count', 'open_issues_count', 'watchers_count')

        # separate full name to list ['owner', 'repository name']
        repo_name = repo['full_name']
        repo_owner_name_list = repo_name.split('/')

        issue_list = GetIssueContent(repo_owner_name_list[0], repo_owner_name_list[1]).get_issue_content()[0:2]
        clean_issue_list = '[[[[[Next]]]]]'.join(map(str, issue_list))
        repo_issue_content_list.append(clean_issue_list)

        # add star count and merge to existing dictionary
        star_count = {
            "star_count": GetStarCountsByRepo(repo['full_name']).get()
        }
        repos_by_lang[index] = py_.merge(repos_by_lang[index], star_count)

    pd_format_dic = {
        'full_name': py_.pluck(repos_by_lang, 'full_name'),
        'forks_count': py_.pluck(repos_by_lang, 'forks_count'),
        'open_issues_count': py_.pluck(repos_by_lang, 'open_issues_count'),
        'watchers_count': py_.pluck(repos_by_lang, 'watchers_count'),
        'comment_count': py_.pluck(repos_by_lang, 'comment_count'),
        'star_count': py_.pluck(repos_by_lang, 'star_count'),
        'issue_content': repo_issue_content_list
    }

    # print(pd_format_dic)
    
    df = pd.DataFrame.from_dict(pd_format_dic)
    file_name = Config().get_search_setting()['lang'].split(':')[1]
    df.to_csv(f'../data/{file_name}_github_{page_num}.csv')
    print(f'Saving {file_name}_github_{page_num} to csv finished!!')


# python do while structure
page = 1
query_string = f"q={Config().get_search_setting()['lang']}&page={page}&per_page={Config().get_search_setting()['data_per_page']}&sort=stars&order=desc"

while True:
    # initial request  
    repos_by_lang = GetReposByLang(query_string).get()

    # store data to csv 
    repos_to_csv(repos_by_lang['body'], page)

    # get response header to form next page query string
    pagination_info = repos_by_lang['pagination']
    next_page_query_string = urlparse.urlparse(unquote(pagination_info['next']['url'])).query
    last_page_query_string = urlparse.urlparse(unquote(pagination_info['last']['url'])).query

    # access to global variable @query_string
    query_string = next_page_query_string
    page = page + 1

    if (next_page_query_string == last_page_query_string):
        repos_by_lang = GetReposByLang(last_page_query_string).get()
        repos_to_csv(repos_by_lang['body'], page)
        break
