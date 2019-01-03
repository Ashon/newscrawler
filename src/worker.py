from collections import defaultdict
from itertools import chain as iter_chain

import mecab
from celery import Celery
from celery import group
from celery import chain
from celery import subtask
from celery import states

from extractors.naver import NaverNewsLinkExtractor
from extractors.naver import NaverNewsContentExtractor

from settings import BROKER_URL
from settings import BACKEND_URL
from settings import SPIDER_CONFIG


app = Celery(__name__, broker=BROKER_URL, backend=BACKEND_URL)

app.conf.task_routes = {
    'worker.harvest_links': {'queue': 'harvest_links'},
    'worker.harvest_content': {'queue': 'harvest_content'},
    'worker.distribute_chain': {'queue': 'distribute_chain'},
    'worker.extract_nouns': {'queue': 'extract_nouns'},
    'worker.aggregate_words': {'queue': 'aggregate_words'}
}

app.conf.task_track_started = True

m = mecab.MeCab()

link_extractor = NaverNewsLinkExtractor(
    **SPIDER_CONFIG['naver']['link_extractor'])

content_extractor = NaverNewsContentExtractor(
    **SPIDER_CONFIG['naver']['content_extractor'])


def map_single_task(args_list, *signatures):
    return group([
        subtask(signatures[0]).clone((args,))
        for args in args_list
    ])


def map_signature_chain(args_list, *signatures):
    return group([
        chain(
            subtask(signatures[0]).clone((args,)),
            *(subtask(sig) for sig in signatures[1:])
        ) for args in args_list
    ])


workflow_resolvers = {1: map_single_task}


@app.task(bind=True, ignore_results=True)
def distribute_chain(self, args_list, *signatures):
    workflow_resolver = workflow_resolvers.get(
        len(signatures), map_signature_chain)

    group_task = workflow_resolver(args_list, *signatures)

    return group_task()


@app.task(bind=True)
def harvest_links(self, sid, date, page):
    news_links = link_extractor.extract(sid=sid, date=date, page=page)

    return news_links['links']


@app.task(bind=True)
def harvest_content(self, extracted_link):
    try:
        news_content = content_extractor.extract(
            link=extracted_link['url'])

        return news_content

    except Exception:
        # Celery Issues: 4222
        self.update_state(state=states.FAILURE)

        return {
            'content': 'NO_CONTENT',
            'date': 'NO_DATE'
        }


@app.task(bind=True)
def extract_nouns(self, extracted_content):
    nouns = m.nouns(extracted_content['content'])

    return nouns


@app.task(bind=True)
def aggregate_words(self, words_lists):
    bag_of_words = defaultdict(int)

    for noun in iter_chain(*words_lists):
        if len(noun) > 1:
            bag_of_words[noun] += 1

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])

    return dict(top_words[-20:])
