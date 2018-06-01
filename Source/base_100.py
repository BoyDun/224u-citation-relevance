import os
import sys
import numpy
import util
import metrics
import concurrent.futures
import random

from collections import OrderedDict

TARGET_PATH = os.path.join('..', 'Data', 'nd')
CANDIDATE_PATH = os.path.join('..', 'Data', 'nd_100')

out = open("recommender_output.txt", 'w')

for target_name in os.listdir(TARGET_PATH):
    print
    out.write('\n')
    target_id = util.id_from_file_name(target_name)
    print 'Computing metrics for case %s...' % (target_id)
    out.write('Computing metrics for case %s...\n' % (target_id))

    target = util.load_opinion(TARGET_PATH, target_name)
    if not metrics.valid_target(target):
        print "Not a valid target. Moving on..."
        out.write('Not a valid target. Moving on...\n')
        continue
    cited_opinions = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_opinion = [executor.submit(util.fetch_opinion_soup, citation) for citation in target.identifier.citations]
        for future in concurrent.futures.as_completed(future_to_opinion):
            if future:
                result = future.result()
                if result is not None:
                    cited_opinions.append(result.text)
#    for citation in target.identifier.citations:
#        opinion = util.fetch_opinion_soup(citation)
#        if opinion is not None:
#            print opinion
#            ascii_text = util.filter_non_ascii(opinion.text)
#            cited_opinions.append(ascii_text)
#            break
#        sys.exit()
    num_opinions = len(cited_opinions)
    if num_opinions <= 1:
        continue
    remove_index = random.randint(0, num_opinions - 1)
    remove_citation = cited_opinions[remove_index]
    del cited_opinions[remove_index]
    scores = OrderedDict()
    counter = 0
    for candidate_name in os.listdir(CANDIDATE_PATH):
        candidate_id = util.id_from_file_name(candidate_name)
        candidate = util.load_opinion(TARGET_PATH, candidate_name)
        if not metrics.valid_candidate(target, candidate):
            scores[candidate_id] = -1
            continue
        counter += 1
        candidate_filtered = util.filter_non_ascii(candidate.html)
        candidate_scores = []
        for cited_opinion in cited_opinions:
            candidate_scores.append(metrics.compute_aggregate_relevance(cited_opinion, candidate_filtered))
        scores[candidate_id] = max(candidate_scores)
        print counter
    
    filtered_remove = util.filter_non_ascii(remove_citation)
    candidate_scores = []
    for cited_opinion in cited_opinions:
        candidate_scores.append(metrics.compute_aggregate_relevance(cited_opinion, filtered_remove))
    scores['KEY'] = max(candidate_scores)

    sorted_scores = sorted(scores, key=scores.get, reverse=True)
    print "Top 5 recommendations:"
    print util.take(5, sorted_scores)
    print "All recommendations:"
    print sorted_scores
    out.write('Top 5 recommendations:\n')
    out.write(str(util.take(5, sorted_scores)))
    out.write('\n\n')
    out.write('All recommendations:\n')
    out.write(str(sorted_scores))
    break
