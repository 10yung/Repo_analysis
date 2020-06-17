import sys
import os
import os.path as path
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.select_cols import SelectCols
from tqdm import tqdm

# get all repo name from mysql preload repo namae
repos_name = SelectCols().col_name('full_name')
repos_name_list = [item[0] for item in repos_name]

def cleantext(unprocessed_issue):
    cleanhtmltag = re.compile('<.*?>')
    exclusionList = [cleanhtmltag, '#', '\[\[\[\[\[Next\]\]\]\]\]']

    result0 = re.sub('http[s]?://\S+', '', unprocessed_issue)
    result1 = re.sub(r"[-()\"△_+'!`%$*#/@;:<>{}=~|.?,]", '', result0)
    result2 = re.sub('\[image\]', '', result1)
    result3 = re.sub('[^a-zA-Z]', ' ', result2)
    result4 = re.sub(r'\s+', ' ', result3)
    result5 = result4.replace("[ ]", "")
    result6 = result5.replace("[x]", "")
    for a in range(0, len(exclusionList)):
        result = re.sub(exclusionList[a], '', result6)

    return result


# save issue comment to repo_name.txt
for repo_name in tqdm(repos_name_list):
    repo_owner_name_list = repo_name.split('/')
    repo_file_name = '_'.join(repo_owner_name_list)
    with open('../data/issue_comment/%s.txt' % repo_file_name, 'r') as file:
        issue_comment = file.read()
        # clean string
        cleaned_issue_comment = cleantext(issue_comment)
        # print(cleaned_issue_comment)
        # 
        with open('../data/clean_issue_comment/%s.txt' % repo_file_name, "wt") as file:
            file.write(cleaned_issue_comment)
