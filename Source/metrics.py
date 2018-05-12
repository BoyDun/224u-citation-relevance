import tfidf

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

def compute_aggregate_relevance(target, candidate):
    
    tfidf_score = 1 * tfidf.tfidf_distance(target, candidate)
    return tfidf_score
