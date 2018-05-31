import numpy as np
import util
import pickle
import os
from scipy.sparse.linalg import norm

if not os.path.exists('../Data/tfidf.pkl'):
  print('ERROR: the TF-IDF transformer is missing.')

with open('../Data/tfidf.pkl', 'rb') as pf:
  transformer = pickle.Unpickler(pf).load()

def tfidf_distance(text1, text2):
  v1 = util.vectorize_opinion(text1)
  v2 = util.vectorize_opinion(text2)
  t1 = transformer.transform(v1)
  t2 = transformer.transform(v2)
  return (t1.dot(t2.T) / (norm(t1) * norm(t2)))[0, 0]
