import sys
import os
import time
import warnings
import gensim

warnings.filterwarnings(action = 'ignore') 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.select_cols import SelectCols
from tqdm import tqdm
from gensim.models import Word2Vec


# get all repo name from mysql preload repo namae
repos_name = SelectCols().col_name('full_name')
repos_name_list = [ item[0] for item in repos_name ]

'''
    If you want to train your own model then use the second line of model. Here we use the pre-trained google news model
'''
model = gensim.models.KeyedVectors.load_word2vec_format('/Users/tengyunglin/Downloads/GoogleNews-vectors-negative300.bin', binary=True)
# model = Word2Vec(unprocessed_issue_content, size=100, window=5, min_count=1, workers=4)


# save issue comment to repo_name.txt
for repo_name in tqdm(repos_name_list):
    repo_owner_name_list = repo_name.split('/')
    repo_file_name = '_'.join(repo_owner_name_list)

    issue_content_vector = []

    with open('../data/clean_issue_comment/%s.txt' % repo_file_name, 'r') as file:
        issue_comment = file.read()
        content_list  = issue_comment.split()

        for word in content_list:
            try:
                vector = model.wv[word]
                vector = vector.tolist()
                issue_content_vector.append(vector)
            except:
                pass
    
        issue_content_vector_str = ','.join(map(str, issue_content_vector))
        issue_content_vector_str = issue_content_vector_str[1:-1]

        with open('../data/word2vec_issue_comment/%s.txt' % repo_file_name, "wt") as file:
            file.write(issue_content_vector_str)
    


    

