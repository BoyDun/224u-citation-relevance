import util
import pickle
import os

if not os.path.exists('../Data/tfidf.pkl'):
  print('ERROR: the TF-IDF transformer is missing.')

with open('../Data/tfidf.pkl', 'rb') as pf:
  transformer = pickle.Unpickler(pf).load()

def tfidf_distance(opinion1, opinion2):
  v1 = util.vectorize_count_dict(opinion1)
  v2 = util.vectorize_count_dict(opinion2)
  t1 = transformer.fit(v1)
  t2 = transformer.fit(v2)
  return t1.dot(t2)
