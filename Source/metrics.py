# -*- coding: utf-8 -*-

#from nltk import ne_chunk, pos_tag, word_tokenize
#from nltk.tree import Tree
from collections import defaultdict
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import numpy.linalg

import tfidf

ST = StanfordNERTagger('/home/bodun/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/home/bodun/stanford-ner-2018-02-27/stanford-ner.jar',
                       encoding='utf-8')

#TODO: ANY OTHER VALID JURISDICTIONS FOR ND?
VALID_ND_SUPREME_COURT_JURSIDICTIONS = set(['nd', 'scotus'])
VALID_JURISDICTIONS = {'nd': VALID_ND_SUPREME_COURT_JURSIDICTIONS}

def valid_target(target):
    id_ = target.identifier
    return id_ is not None and id_.datetime is not None and id_.jurisdiction is not None and id_.citations

def valid_candidate(target, candidate):
    target_jur = target.identifier.jurisdiction
    candidate_jur = candidate.identifier.jurisdiction
    if candidate_jur not in VALID_JURISDICTIONS[target_jur]:
	return False
    return candidate.datetime < target.datetime

def get_entities(text):
    """
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        print i
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append((named_entity, i.label()))
                current_chunk = []
            else:
                continue
    organization_entities = defaultdict(int)
    for pair in continuous_chunk:
        if pair[1] == 'organization': #TODO: WHAT IS ACTUAL ORGANIZATION LABEL?
            organization_entities[pair[0]] += 1
    return organization_entities
    """
    tokenized_text = word_tokenize(text)
    classified_text = ST.tag(tokenized_text)
    organization_entities = defaultdict(int)
    for word, entity in classified_text:
        if entity == 'ORGANIZATION':
            organization_entities[word] += 1
    return organization_entities

def calc_entity_distance(cited_text, candidate):
    cited_entities = get_entities(cited_text)
    candidate_entities = get_entities(candidate.html)
    overlap = 0.0
    for entity in cited_entities:
        if entity in candidate_entities:
            overlap += cited_entities[entity] * candidate_entities[entity]
    distance = overlap / (numpy.linalg.norm(cited_entities.values()) * numpy.linalg.norm(candidate_entities.values()))
    return distance

def compute_aggregate_relevance(cited_text, candidate):
    entity_score = 1 * calc_entity_distance(cited_text, candidate)
    tfidf_score = 1 * tfidf.tfidf_distance(cited_text, candidate)
    return tfidf_score + entity_score
