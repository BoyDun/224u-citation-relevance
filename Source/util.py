import pickle
import os
import urllib2
import requests
import BeautifulSoup as bs

from itertools import islice

def id_from_file_name(name):
    return name.split('.')[0]

def load_opinion(directory, file_name):
    full_file_path = os.path.join(directory, file_name)
    return pickle.Unpickler(open(full_file_path, 'rb')).load()

def fetch_opinion(citation):
    if not citation._reporter or not citation._volume or not citation._page:
        return None
    
    url_base = 'https://courtlistener.com/c/'
    url_base += citation._reporter + '/'
    url_base += citation._volume + '/'
    url_base += citation._page + '/'
    #url_base = 'https://www.courtlistener.com/c/U.S./100/43/'
    #url_base = 'https://www.courtlistener.com/c/U.S./558/310/'
    r = requests.get(url_base, allow_redirects=False)
    if r.status_code == 404:
        print '404 Error: Citation Not Found'
        return None
    elif r.status_code == 301:
        r = requests.get(url_base)
        soup = bs.BeautifulSoup(r.content)
        return soup.find("div", {"id": "opinion-content"})
    elif r.status_code == 200:
        print 'Multiple results found. Skipping for speed...'
        return None
    else:
        raise ValueError('UNCAUGHT STATUS CODE: ' + str(r.status_code))

def take(n, iterable):
    return list(islice(iterable, n))
