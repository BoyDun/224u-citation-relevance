import pickle
import os
import urllib2
import requests
from bs4 import BeautifulSoup as bs
import enchant 
import sklearn
import re
import string

from itertools import islice
from collections import Counter

def id_from_file_name(name):
    return name.split('.')[0]

def load_opinion(directory, file_name):
    full_file_path = os.path.join(directory, file_name)
    return pickle.Unpickler(open(full_file_path, 'rb')).load()

def fetch_opinion_soup(citation):
    print 'called fetch'
    if not citation._reporter or not citation._volume or not citation._page:
        return None
    
    url_base = 'https://courtlistener.com/c/'
    url_base += citation._reporter + '/'
    url_base += citation._volume + '/'
    url_base += citation._page + '/'
    r = requests.get(url_base, allow_redirects=False)
    if r.status_code == 404:
        print '404 Error: Citation Not Found'
        return None
    elif r.status_code == 301:
        r = requests.get(url_base)
        soup = bs(r.content, 'html5lib')
        opinion = soup.find("div", {"id": "opinion-content"})
        return opinion
    elif r.status_code == 200:
        print 'Multiple results found. Skipping for speed...'
        return None
    else:
        raise ValueError('UNCAUGHT STATUS CODE: ' + str(r.status_code))

def tokens_from_opinion(opinion):
    soup = bs(opinion, 'html5lib')
    text = soup.get_text()
    text = re.sub(r'[^\w\s]','', text)
    text = text.lower()
    words = text.split()
    return words

word_list = enchant.Dict("en_US")

def is_english_word(word):
    return word_list.check(word)

def word_counts_from_tokens(tokens):
    words = [word for word in tokens if word.isalpha() and is_english_word(word)]
    counts = Counter(words)
    return counts

with open('../Data/count_vectorizer.pkl', 'rb') as pf:
    count_vectorizer = pickle.Unpickler(pf).load()

def vectorize_count_dict(count_dict):
    return count_vectorizer.transform(count_dict)

def vectorize_opinion(opinion):
    tokens = tokens_from_opinion(opinion)
    word_counts = word_counts_from_tokens(tokens)
    count_vector = vectorize_count_dict(word_counts)
    return count_vector

def take(n, iterable):
    return list(islice(iterable, n))

def filter_non_ascii(text):
    printable = set(string.printable)
    return filter(lambda x: x in printable, text)
