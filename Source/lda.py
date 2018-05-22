import pickle
import sys
import objects
import string
import re
import enchant
from bs4 import BeautifulSoup
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter
from sklearn.feature_extraction import DictVectorizer

import numpy as np

import os
import tfidf

data_dir = '../Data/nd'

filenames = os.listdir(data_dir)
filepaths = [os.path.join(data_dir, filename) for filename in filenames]
num_files = len(filenames)


for pkl in [filepaths[0], '../Data/nd/1707959.pkl']:
    with open(pkl, "rb") as pickle_file:
        unpickler = pickle.Unpickler(pickle_file)
        print(unpickler.load().html)



count_dicts = []
ops = []

for i, pkl in enumerate(filepaths[:1000]):
    with open('./' + pkl, "rb") as pickle_file:
        unpickler = pickle.Unpickler(pickle_file)
        ops.append(unpickler.load())

prox = [tfidf.tfidf_distance(ops[0].html, i) for i in ops]
print(filepaths[np.argmax(prox) + 1])


'''
        soup = BeautifulSoup(j.html, 'lxml')
        text = soup.get_text()
        # text = text.translate(None, string.punctuation)
        text = re.sub(r'[^\w\s]','', text)
        text = text.lower()
        words = text.split()
        words = [word for word in words if word.isalpha()]
        counts = Counter(words)
        count_dicts.append(counts)
    print "processed " + pkl + ": " + str(i) + "/" + str(num_files)
'''


'''
with open('../Data/count_dicts_nd.py', 'rb') as wc_file:
    unpickler = pickle.Unpickler(wc_file)
    count_dicts = unpickler.load()

print('unpickler loaded')
w = enchant.Dict("en_US")

for i, count_dict in enumerate(count_dicts):
    for key in count_dict.keys():
        if not w.check(key) or not key.isalpha():
            del count_dict[key]

v = DictVectorizer(sparse = True)
X = v.fit_transform(count_dicts)
fnames = v.get_feature_names()
with open('../Data/feature_names.pkl', 'wb') as fn_file:
    pickle.dump(fnames, fn_file)
'''


'''
with open('../Data/tfidf_matrix.pkl', 'rb') as wc_file:
    unpickler = pickle.Unpickler(wc_file)
    X = unpickler.load()

with open('../Data/feature_names.pkl', 'rb') as feature_names_file:
    unpickler = pickle.Unpickler(feature_names_file)
    fn = unpickler.load()

lda = LatentDirichletAllocation(n_components=5, learning_method = 'online')
ft = lda.fit_transform(X)

'''
