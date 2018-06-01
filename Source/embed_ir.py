import numpy as np
import pickle
from gensim.models import KeyedVectors
from sklearn.feature_extraction import DictVectorizer
import util


wv = KeyedVectors.load_word2vec_format('../Data/GoogleNews-vectors-negative300.bin',
                       binary=True,
                       limit=500000)

with open('../Data/count_dicts_nd.pkl', 'rb') as wc_file:
    unpickler = pickle.Unpickler(wc_file)
    count_dicts = unpickler.load()

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

nameset = set(feature_names)
name_filter = [name in nameset for name in v.get_feature_names()]
indices = np.array(name_filter).nonzero()[0]
X_words = X[:, indices]

X_mentions = X_words != 0
df = np.sum(X_mentions, axis=0)
N = X_mentions.shape[1]

idf = np.log(1 + N / df).T
idf = np.array(idf)

sum_embed = X_words.dot(np.array(embeddings) * idf)
num_words = X_words.dot(np.array(represented).reshape((-1, 1)) * idf)
num_words = np.reshape(num_words, (-1, 1))
case_embeddings = sum_embed / num_words

case_embeddings_norm = np.sqrt(np.sum(np.square(case_embeddings), axis=1))
len(case_embeddings_norm)
target_embedding_norm = np.linalg.norm(case_embeddings[0])

cosine_sim = case_embeddings.dot(case_embeddings[0].T) / (case_embeddings_norm * target_embedding_norm)
