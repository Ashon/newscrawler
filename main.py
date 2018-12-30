import time
from datetime import datetime
from itertools import chain

import celery

import sys
sys.path.append('src')  # noqa: E402

from worker import dmap
from worker import harvest_links
from worker import harvest_content
from worker import extract_nouns
from worker import aggregate_words

MAX_PAGES_PER_DATE = 30


def main():
    today = datetime.now().strftime('%Y%m%d')
    print(today)

    workflows = [(
        harvest_links.s(today, page) | dmap.s(harvest_content.s())
    )() for page in range(MAX_PAGES_PER_DATE)]
    print(workflows)

    # wait for getting group_result
    chain_results = [chain.get() for chain in workflows]

    # get group_results
    chain_results = [chain.children[0] for chain in workflows]
    print(chain_results)

    # get harvest_content results from group_result in workflows
    articles = chain(*[
        chain.children[0].get() for chain in workflows
    ])
    print(articles)

    # aggregate nouns and get top 20 ranked words
    aggregate_job = celery.chord(
        extract_nouns.s(article) for article in articles
    )(aggregate_words.s())

    bows = aggregate_job.get()
    print(bows)


if __name__ == '__main__':
    start = time.time()
    main()
    duration = time.time() - start
    print(duration)
