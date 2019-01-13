from collections import defaultdict
from itertools import chain as iter_chain

import mecab
from celery import states

from extractors.naver import NaverNewsLinkExtractor
from extractors.naver import NaverNewsContentExtractor

from core.app import initialize_applictaion
from core.workflows import distribute_chain

import settings


app = initialize_applictaion(settings)

m = mecab.MeCab()

link_extractor = NaverNewsLinkExtractor(
    **settings.SPIDER_CONFIG['naver']['link_extractor'])

content_extractor = NaverNewsContentExtractor(
    **settings.SPIDER_CONFIG['naver']['content_extractor'])

# add workflow util task
distribute_chain = app.task(bind=True, ignore_results=True)(distribute_chain)


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
