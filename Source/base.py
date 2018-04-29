import os
import sys
import numpy
import util
import metrics

from collections import OrderedDict

DATA_PATH = os.path.join('..', 'Data', 'nd')

for target_name in os.listdir(DATA_PATH):
    print
    target_id = util.id_from_file_name(target_name)
    print 'Computing metrics for case %s...' % (target_id)

    target = util.load_opinion(DATA_PATH, target_name)
    if not target.identifier.citations:
        print "No citations. Moving on..."
        continue

    cited_opinions = []
    for citation in target.identifier.citations:
        opinion = util.fetch_opinion(citation)
        if opinion:
            cited_opinions.append(opinion)

    scores = OrderedDict()
    for candidate_name in os.listdir(DATA_PATH):
        candidate_id = util.id_from_file_name(candidate_name)
        candidate = util.load_opinion(DATA_PATH, candidate_name)
        candidate_scores = []
        for cited_opinion in cited_opinions:
            candidate_scores.append(metrics.compute_aggregate_relevance(cited_opinion, candidate))
        scores[candidate_id] = max(candidate_scores)

    sorted_scores = sorted(scores, key=scores.get, reverse=True)
    print "Top 10 recommendations:"
    print util.take(10, sorted_scores)
