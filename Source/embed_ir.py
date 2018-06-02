import numpy as np
import pickle
from gensim.models import KeyedVectors
from sklearn.feature_extraction import DictVectorizer
import util
from collections import Counter

print('loading embeddings data...')

wv = KeyedVectors.load_word2vec_format('../Data/GoogleNews-vectors-negative300.bin',
                       binary=True,
                       limit=500000)

print('loading count dicts...')

with open('../Data/count_dicts_nd.pkl', 'rb') as wc_file:
    unpickler = pickle.Unpickler(wc_file)
    count_dicts = unpickler.load()

print('performing vectorization...')
    
v = DictVectorizer(sparse = True)
X = v.fit_transform(count_dicts)

def get_embed(word):
    if word in wv:
        return wv[word]
    else:
        return np.zeros((300))
    
def represented_word(word):
    return 1 if word in wv else 0

with open('../Data/feature_names.pkl', 'rb') as fn_file:
    unpickler = pickle.Unpickler(fn_file)
    feature_names = unpickler.load()

embeddings = [get_embed(word) for word in feature_names]
represented = [represented_word(word) for word in feature_names]

print('computing IDF...')

nameset = set(feature_names)
name_filter = [name in nameset for name in v.get_feature_names()]
indices = np.array(name_filter).nonzero()[0]
X_words = X[:, indices]

X_mentions = X_words != 0
df = np.sum(X_mentions, axis=0)
N = X_mentions.shape[1]

# parametrize me!
idf = (1 + N / df).T
idf = np.array(idf)

print('computing PC1...')

def freqs_to_embeds(vect):
    sum_embed = vect.dot(np.array(embeddings) * idf)
    num_words = vect.dot(np.array(represented).reshape((-1, 1)) * idf)
    num_words = np.reshape(num_words, (-1, 1))
    return sum_embed / num_words  

# these are used to find the PCA.
case_embeddings = freqs_to_embeds(X_words)

from sklearn.decomposition import PCA
pca = PCA(n_components=1)
pca.fit(case_embeddings)
pc1 = pca.components_

# common component removal. see arora, liang, and ma (2016)
def cr(v, pc1):
    alignment = v.dot(pc1.T) / pc1.dot(pc1.T)
    return v - alignment * pc1

def ccr(v):
    return cr(v, pca.components_)

def embed_word_list(words):
    words = [w.lower() for w in words]
    count_dict = Counter(words)
    vect = v.transform(count_dict).toarray()
    vect = vect[:, indices]
    
    case_embed = freqs_to_embeds(vect)
    return ccr(case_embed)

def cosine_sim(x, y):
    x_norm = np.linalg.norm(x, axis=1)
    y_norm = np.linalg.norm(y, axis=1)
    return x.dot(y.T) / (x_norm * y_norm)

# begin test code

target = 0

cet = case_embeddings[target].reshape((1, -1))
cosine_similarity = cosine_sim(cet, case_embeddings)
print(cosine_similarity)

best_match = np.argsort(cosine_similarity)[0, -2]

import os 
data_dir = '../Data/nd'
filenames = os.listdir(data_dir)
found_names = [filenames[target], filenames[best_match]]
print(found_names)

for pkl in found_names:
    pklf = os.path.join(data_dir, pkl)
    with open(pklf, "rb") as pickle_file:
        unpickler = pickle.Unpickler(pickle_file)
        print(unpickler.load().html)
    for i in range(20):
        print

