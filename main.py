import pprint
import time
from collections import defaultdict
from datetime import datetime
from itertools import chain
from itertools import product

import celery
import halo

import sys
sys.path.append('src')  # noqa: E402

from worker import distribute_chain
from worker import harvest_links
from worker import harvest_content
from worker import extract_nouns
from worker import aggregate_words

from worker import content_extractor


MAX_PAGES_PER_DATE = 30

NAVER_NEWS_SECSIONS = [
    '001',  # Headline
    '100',  # Politics
    '101',  # Economics
    '102',  # Society
    '103',  # Culture / Life
    '104',  # World
    '105',  # Science
]


def wait_tasks(group_results, msg):
    with halo.Halo(text=msg) as spinner:
        start = time.time()

        while not all([task.ready() for task in group_results]):
            time.sleep(1)

            state_dict = defaultdict(int)
            for group_result in group_results:
                for async_result in group_result.children:
                    state_dict[async_result.state] += 1

            spinner.text = f'{msg} - {dict(state_dict)}'

        elapsed = time.time() - start
        spinner.succeed(f'{msg} - Done ({len(group_results)} tasks / {elapsed:.2f}s)')


def harvest_and_analyze():
    today = datetime.now().strftime('%Y%m%d')

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

    wait_tasks(
        group_results=[workflow],
        msg='Wait for workflow group tasks..')

    wait_tasks(
        group_results=workflow.children,
        msg='Wait for Chain tasks ready..')

    wait_tasks(
        group_results=[subtask.children[0] for subtask in workflow.children],
        msg='Wait for Terminal tasks ready..')

    # get word lists from workflows
    results = [subtask.children[0].get() for subtask in workflow.children]
    words = list(set([tuple(x) for x in chain(*results)]))

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
