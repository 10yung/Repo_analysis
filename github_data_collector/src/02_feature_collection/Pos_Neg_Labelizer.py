from numpy import array
from string import punctuation
from os import listdir
from os.path import dirname, realpath

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tqdm import tqdm
from utils.create_cols import CreateCols
from utils.insert_update import InsertUpdate

from utils.select_cols import SelectCols
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json


# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text


# turn a doc into clean tokens
def clean_doc(doc):
    # split into tokens by white space
    tokens = doc.split()
    # remove punctuation from each token
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # filter out short tokens
    tokens = [word for word in tokens if len(word) > 1]
    return tokens


# load doc, clean and return line of tokens
def doc_to_line(filename, vocab):
    # load the doc
    doc = load_doc(filename)
    # clean doc
    tokens = clean_doc(doc)
    # filter by vocab
    tokens = [w for w in tokens if w in vocab]
    return ' '.join(tokens)


# load all docs in a directory
def process_docs(directory, vocab, is_trian):
    lines = list()
    # walk through all files in the folder
    for filename in listdir(directory):
        # skip any reviews in the test set
        if is_trian and filename.startswith('cv9'):
            continue
        if not is_trian and not filename.startswith('cv9'):
            continue
        # create the full path of the file to open
        path = directory + '/' + filename
        # load and clean the doc
        line = doc_to_line(path, vocab)
        # add to list
        lines.append(line)
    return lines

# Define project root directory
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
# load the vocabulary
vocab_filename = project_path + '/ml_model/vocab.txt'
vocab = load_doc(vocab_filename)
vocab = vocab.split()
vocab = set(vocab)
# load all training reviews
positive_lines = process_docs('../data/txt_sentoken/pos', vocab, True)
negative_lines = process_docs('../data/txt_sentoken/neg', vocab, True)
# create the tokenizer
tokenizer = Tokenizer()
# fit the tokenizer on the documents
docs = negative_lines + positive_lines
tokenizer.fit_on_texts(docs)
# encode training data set
Xtrain = tokenizer.texts_to_matrix(docs, mode='freq')
ytrain = array([0 for _ in range(900)] + [1 for _ in range(900)])

# load all test reviews
positive_lines = process_docs('../data/txt_sentoken/pos', vocab, False)
negative_lines = process_docs('../data/txt_sentoken/neg', vocab, False)
docs = negative_lines + positive_lines
# encode training data set
Xtest = tokenizer.texts_to_matrix(docs, mode='freq')
ytest = array([0 for _ in range(100)] + [1 for _ in range(100)])

n_words = Xtest.shape[1]

# load json and create model

model_json_path = project_path + '/ml_model/model.json'
json_file = open(model_json_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model

model_path = project_path + '/ml_model/movie_review_model'
loaded_model.load_weights(model_path)
print("Loaded model from disk")


# classify a review as negative (0) or positive (1)
def predict_sentiment(review, vocab, tokenizer, loaded_model):
    # clean
    tokens = clean_doc(review)
    # filter by vocab
    tokens = [w for w in tokens if w in vocab]
    # convert to line
    line = ' '.join(tokens)
    # encode
    encoded = tokenizer.texts_to_matrix([line], mode='freq')
    # prediction
    yhat = loaded_model.predict(encoded, verbose=0)
    return round(yhat[0, 0])


repos_name = SelectCols().col_name('full_name')
repos_name_list = [item[0] for item in repos_name]

# Select github repos full name from db
repos_name = SelectCols().col_name('full_name')
repos_name_list = [item[0] for item in repos_name]

create_column = CreateCols().create_cols({
    "colName": "Good_or_Bad",
    "type": "INT"
})

for repo_name in tqdm(repos_name_list):
    # convert '/' to '_'
    repo_owner_name_list = repo_name.split('/')
    reop_txt_name = '_'.join(repo_owner_name_list)

    # read file base on repo name
    with open('../data/clean_issue_comment/%s.txt' % reop_txt_name, 'r') as file:
        issue_comment = file.read()

        # transform text to negative(0) positive(1) label
        pos_neg_label = predict_sentiment(issue_comment, vocab, tokenizer, loaded_model)
        pos_neg_label = int(pos_neg_label)
        InsertUpdate('Good_or_Bad').update_val(repo_name, pos_neg_label)
