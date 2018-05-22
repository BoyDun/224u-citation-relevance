import os
import sys
import numpy
import util
import metrics
import concurrent.futures

from collections import OrderedDict

DATA_PATH = os.path.join('..', 'Data', 'nd')

for target_name in os.listdir(DATA_PATH):
    print
    target_id = util.id_from_file_name(target_name)
    print 'Computing metrics for case %s...' % (target_id)

    target = util.load_opinion(DATA_PATH, target_name)
    if not metrics.valid_target(target):
        print "Not a valid target. Moving on..."
        continue
    target.html = util.filter_non_ascii(target.html)
    cited_opinions = []
#    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
#        future_to_opinion = [executor.submit(util.fetch_opinion_soup, citation) for citation in target.identifier.citations]
#        for future in concurrent.futures.as_completed(future_to_opinion):
#            if future:
#                result = future.result()
#                if result is not None:
#                    cited_opinions.append(result.text)
    for citation in target.identifier.citations:
        opinion = util.fetch_opinion_soup(citation)
        if opinion is not None:
            print opinion
            ascii_text = util.filter_non_ascii(opinion.text)
            cited_opinions.append(ascii_text)
            break
#        sys.exit()
    print len(cited_opinions)
    scores = OrderedDict()
    for candidate_name in os.listdir(DATA_PATH):
        candidate_id = util.id_from_file_name(candidate_name)
        candidate = util.load_opinion(DATA_PATH, candidate_name)
        if not metrics.valid_candidate(target, candidate):
            scores[candidate_id] = -1
            continue
        candidate_scores = []
        for cited_opinion in cited_opinions:
            candidate_scores.append(metrics.compute_aggregate_relevance(cited_opinion, candidate))
        scores[candidate_id] = max(candidate_scores)

    sorted_scores = sorted(scores, key=scores.get, reverse=True)
    print "Top 10 recommendations:"
    print util.take(10, sorted_scores)
