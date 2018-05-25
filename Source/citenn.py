import tensorflow as tf

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

import util

data_dir = '../Data/nd'

filenames = os.listdir(data_dir)
filepaths = [os.path.join(data_dir, filename) for filename in filenames]
num_files = len(filenames)

labels = tf.placeholder(dtype=tf.float32, shape=(None, 1)) # one-hot 0/1
vectors = tf.placeholder(dtype=tf.float32, shape=(None, 36124))
representation = tf.layers.dense(vectors, 500, tf.nn.relu)
doubled_representation = tf.reshape(representation, shape=(-1, 1000))

fc1 = tf.layers.dense(doubled_representation, 500, activation=tf.nn.relu)
fc2 = tf.layers.dense(fc1, 300, activation=tf.nn.relu)
fc3 = tf.layers.dense(fc2, 100, activation=tf.nn.relu)

logit = tf.layers.dense(fc3, 1, activation=None)

'''
# etc etc
cost = None # what goes here?
'''

cost = tf.nn.sigmoid_cross_entropy_with_logits(labels = labels, logits = logit)
cost = tf.reduce_mean(cost)

opt = tf.train.AdamOptimizer(1e-2)
train_op = opt.minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

def train_classifier(v, l):
  c, _ = sess.run([logit, train_op], feed_dict={vectors: v, labels: l})
  return c

vecs = []
for pkl in [filepaths[0], '../Data/nd/1707959.pkl', '../Data/nd/1707959.pkl', filepaths[0]]:
  with open(pkl, "rb") as pickle_file:
    unpickler = pickle.Unpickler(pickle_file)
    vec = util.vectorize_opinion(unpickler.load().html)
    vecs.append(vec.toarray())

lab = [[0], [1]]
for i in range(1000):
  print(train_classifier(np.concatenate(vecs, axis=0), lab))

      

