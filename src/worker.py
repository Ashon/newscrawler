from collections import defaultdict
from itertools import chain

import celery
import mecab

from core.extractor import PageExtractor
from extractors import NaverNewsPageExtractor

import settings


app = celery.Celery(
    __name__,
    broker=settings.BROKER_URL,
    backend=settings.BACKEND_URL)

m = mecab.MeCab()

link_extractor = PageExtractor(
    **settings.SPIDER_CONFIG['naver']['news_list'])

content_extractor = NaverNewsPageExtractor(
    **settings.SPIDER_CONFIG['naver']['news_page'])


@app.task
def harvest_links(date, page):
    news_links = link_extractor.extract(date=date, page=page)

    return [{
        'text': link.text,
        'link': link['href']
    } for link in news_links]


@app.task
def dmap(args, signature):
    return celery.group(
        celery.signature(
            varies=signature['task'],
            args=(arg,)
        ) for arg in args
    )()


@app.task
def harvest_content(link_item):
    news_content = content_extractor.extract(link=link_item['link'])

    return news_content


@app.task
def extract_nouns(text):
    nouns = m.nouns(text)

    return nouns


@app.task
def aggregate_words(word_lists):
    bag_of_words = defaultdict(int)

    for noun in chain(*word_lists):
        bag_of_words[noun] += 1

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])

    return dict(top_words[-20:])
