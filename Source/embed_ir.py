import numpy as np
import pickle
from gensim.models import KeyedVectors

wv = KeyedVectors.load_word2vec_format('../Data/GoogleNews-vectors-negative300.bin',
                       binary=True)

with open('../Data/count_dicts_nd.py', 'rb') as wc_file:
    unpickler = pickle.Unpickler(wc_file)
    count_dicts = unpickler.load()


