import pprint
import time
from datetime import datetime
from itertools import chain
from itertools import product

import celery

import sys
sys.path.append('src')  # noqa: E402

from worker import distribute_chain
from worker import harvest_links
from worker import harvest_content
from worker import extract_nouns
from worker import aggregate_words

from worker import content_extractor


MAX_PAGES_PER_DATE = 10

NAVER_NEWS_SECSIONS = [
    '001',  # Headline
    '100',  # Politics
    '101',  # Economics
    '102',  # Society
    '103',  # Culture / Life
    '104',  # World
    '105',  # Science
]


def harvest_and_analyze():
    today = datetime.now().strftime('%Y%m%d')
    # print(today)

    iter_product = product(range(MAX_PAGES_PER_DATE), NAVER_NEWS_SECSIONS)

    workflow = celery.group(
        celery.chain(
            harvest_links.s(sid, today, page),
            distribute_chain.s(
                harvest_content.s(),
                extract_nouns.s()
            )
        ) for page, sid in iter_product
    )()

    print(1)
    workflow.get(interval=1, on_interval=lambda :print(time.time()))
    print(2)
    workflow.children[0].get()
    print(3)
    results = workflow.children[0].children[0].get()

    # get word lists from workflows
    words = list(
        set([
            tuple(x) for x in chain(results)
        ])
    )

    # aggregate nouns and get top 20 ranked words
    aggregate_job = aggregate_words.apply_async(args=(words,))
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
    url = (
        'https://news.naver.com/main/read.nhn?'
        'mode=LSD&mid=sec&sid1=001&oid=030&aid=0002772003'
    )
    content = content_extractor.extract(link=url)
    print(content)


if __name__ == '__main__':
    start = time.time()
    harvest_and_analyze()
    # get_links()
    # test_harvest_content()
    duration = time.time() - start
    print(duration)
