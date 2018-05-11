
#TODO: ANY OTHER VALID JURISDICTIONS FOR ND?
VALID_ND_SUPREME_COURT_JURSIDICTIONS = set(['nd', 'scotus'])
VALID_JURISDICTIONS = {'nd': VALID_ND_SUPREME_COURT_JURSIDICTIONS}

def valid(target, candidate):
    target_jur = target.identifier.jurisdiction
    candidate_jur = candidate.identifier.jurisdiction
    if candidate_jur not in VALID_JURISDICTIONS[target_jur]:
        return False
    return candidate.datetime < target.datetime

def compute_aggregate_relevance(target, candidate):
    raise NotImplementedError()
    return 0
