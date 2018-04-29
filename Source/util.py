import pickle
import os

from itertools import islice

def id_from_file_name(name):
    return name.split('.')[0]

def load_opinion(directory, file_name):
    full_file_path = os.path.join(directory, file_name)
    return pickle.Unpickler(open(full_file_path, 'rb')).load()

def fetch_opinion(citation):
    raise NotImplementedError()

def take(n, iterable):
    return list(islice(iterable, n))
