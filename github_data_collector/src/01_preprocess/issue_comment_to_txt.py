import sys
import os
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.select_cols import SelectCols
from utils.get_issue_content_by_repo import GetIssueContent

# Select github repos full name from db
repos_name = SelectCols().col_name('full_name')
repos_name_list = [item[0] for item in repos_name]

repos_name_list = repos_name_list[0:]

# use repos full name to append issue comment
for repo_name in tqdm(repos_name_list):
    repo_owner_name_list = repo_name.split('/')
    issue_list = GetIssueContent(repo_owner_name_list[0], repo_owner_name_list[1]).get_issue_content()[0:10]
    clean_issue = '\n'.join(map(str, issue_list))
    with open('../data/issue_comment/%s.txt' % '_'.join(repo_owner_name_list), "wt") as file:
        file.write(clean_issue)
