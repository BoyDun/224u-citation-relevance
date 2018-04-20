import pickle
import sys
import objects
import string
import re
from bs4 import BeautifulSoup
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter
from sklearn.feature_extraction import DictVectorizer

pickles = ['194919.pkl', '195561.pkl', '11.pkl']
# encoded with py2?

count_dicts = []
for pkl in pickles:
    pickle_file = open('./' + pkl, "rb")
    unpickler = pickle.Unpickler(pickle_file)
    j = unpickler.load()
    soup = BeautifulSoup(j.html, 'lxml')
    text = soup.get_text()
    # text = text.translate(None, string.punctuation)
    text = re.sub(r'[^\w\s]','', text)
    text = text.lower()
    words = text.split()
    counts = Counter(words)
    count_dicts.append(counts)

v = DictVectorizer(sparse = False)
X = v.fit_transform(count_dicts)

lda = LatentDirichletAllocation(n_components=5, learning_method = 'online')
print(lda.fit_transform(X))

