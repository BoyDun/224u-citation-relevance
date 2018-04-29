import pickle
import os
import urllib2

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
#    url_base = 'https://www.courtlistener.com/c/U.S./100/43/'
    response = urllib2.urlopen(url_base)
    print response.getcode()
    html = response.read()
    print html
    raise NotImplementedError()

def take(n, iterable):
    return list(islice(iterable, n))
