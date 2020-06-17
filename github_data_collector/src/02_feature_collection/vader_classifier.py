import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.select_cols import SelectCols
from utils.create_cols import CreateCols
from utils.insert_update import InsertUpdate
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

'''
    If there is no column inside your table for the word2vec vector result. 
    Uncomments the following line to `Create Column if not exist`
'''
create_column = CreateCols().create_cols(
    {
        "colName": "vader_setimental_result",
        "type": "FLOAT"
    }
)


# get all repo name from mysql preload repo namae
repos_name = SelectCols().col_name('full_name')
repos_name_list = [ item[0] for item in repos_name ]

# save issue comment to repo_name.txt
for repo_name in tqdm(repos_name_list):
    repo_owner_name_list = repo_name.split('/')
    repo_file_name = '_'.join(repo_owner_name_list)

    # open clean issue txt file
    with open('../data/clean_issue_comment/%s.txt' % repo_file_name, 'r') as file:
        # cleaned issue comment string
        clean_issue_comment = file.read()

        analyzer = SentimentIntensityAnalyzer()
        result = analyzer.polarity_scores(clean_issue_comment)
        InsertUpdate('vader_setimental_result').update_val(repo_name, result['compound'])