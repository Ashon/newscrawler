import time
from datetime import datetime
from itertools import chain
import pprint

import celery

import sys
sys.path.append('src')  # noqa: E402

from worker import dmap
from worker import harvest_links
from worker import harvest_content
from worker import extract_nouns
from worker import aggregate_words

from worker import content_extractor


MAX_PAGES_PER_DATE = 1


def harvest_and_analyze():
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
    pprint.pprint(bows)


def get_links():
    today = datetime.now().strftime('%Y%m%d')
    print(today)

    workflows = celery.group(
        harvest_links.s(today, page)
        for page in range(MAX_PAGES_PER_DATE)
    )()
    print(workflows)

    links = workflows.get()
    pprint.pprint(links)


def test_harvest_content():
    url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=001&oid=030&aid=0002772003'
    content = content_extractor.extract(link=url)
    print(content)


if __name__ == '__main__':
    start = time.time()
    harvest_and_analyze()
    # get_links()
    # test_harvest_content()
    duration = time.time() - start
    print(duration)
