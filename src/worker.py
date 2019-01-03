from collections import defaultdict
from itertools import chain

import celery
import mecab

from extractors.naver import NaverNewsLinkExtractor
from extractors.naver import NaverNewsContentExtractor

import settings


app = celery.Celery(
    __name__,
    broker=settings.BROKER_URL,
    backend=settings.BACKEND_URL)

app.conf.task_routes = {
    'worker.harvest_links': {
        'queue': 'harvest_links'
    },
    'worker.harvest_content': {
        'queue': 'harvest_content'
    },
    'worker.distribute_chain': {
        'queue': 'distribute_chain'
    },
    'worker.extract_nouns': {
        'queue': 'extract_nouns'
    },
    'worker.aggregate_words': {
        'queue': 'aggregate_words'
    }
}

app.conf.task_track_started = True

m = mecab.MeCab()

link_extractor = NaverNewsLinkExtractor(
    **settings.SPIDER_CONFIG['naver']['news_list'])

content_extractor = NaverNewsContentExtractor(
    **settings.SPIDER_CONFIG['naver']['news_page'])


@app.task(bind=True)
def harvest_links(self, sid, date, page):
    news_links = link_extractor.extract(sid=sid, date=date, page=page)

    return news_links['links']


@app.task(bind=True)
def distribute_chain(self, args, *signatures):
    if len(signatures) == 1:
        subtasks = [
            celery.signature(
                varies=signatures[0]['task'], args=(arg,)
            ) for arg in args
        ]
    else:
        subtasks = [
            celery.chain(
                celery.signature(
                    varies=signatures[0]['task'], args=(arg,)
                ), *(
                    celery.signature(varies=signature['task'])
                    for signature in signatures[1:]
                )
            ) for arg in args
        ]

    return celery.group(subtasks)()


@app.task(bind=True)
def harvest_content(self, extracted_link):
    try:
        news_content = content_extractor.extract(
            link=extracted_link['url'])

        return news_content

    except Exception as e:
        # Celery Issues:#4222
        self.update_state(state=celery.states.FAILURE)
        return {
            'content': 'NO_CONTENT',
            'date': 'NO_DATE'
        }


@app.task(bind=True)
def extract_nouns(self, extracted_content):
    nouns = m.nouns(extracted_content['content'])

    return nouns


@app.task(bind=True)
def aggregate_words(self, word_lists):
    bag_of_words = defaultdict(int)

    for noun in chain(*word_lists):
        if len(noun) > 1:
            bag_of_words[noun] += 1

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])

    return dict(top_words[-20:])
