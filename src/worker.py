from collections import defaultdict
from itertools import chain as iter_chain

import mecab
from celery import current_app
from celery import states

from core.app import initialize_applictaion
from core.workflows import distribute_chain

import settings


app = initialize_applictaion(settings)

m = mecab.MeCab()

# add workflow util task
distribute_chain = app.task(bind=True, ignore_results=True)(distribute_chain)


@app.task(bind=True)
def harvest_links(self, *args, harvester, **kwargs):
    link_extractor = current_app.extractors[harvester]['link']
    news_links = link_extractor.extract(**kwargs)

    return news_links['links']


@app.task(bind=True)
def harvest_content(self, link, *args, harvester):
    content_extractor = current_app.extractors[harvester]['content']

    try:
        news_content = content_extractor.extract(link=link['url'])

        return news_content

    except Exception:
        # Celery Issues: 4222
        self.update_state(state=states.FAILURE)

        return {
            'content': 'NO_CONTENT',
            'date': 'NO_DATE'
        }


@app.task(bind=True)
def extract(self, extracted_content, *args, method):
    method = getattr(m, method)
    nouns = method(extracted_content['content'])

    return nouns


@app.task(bind=True)
def aggregate_words(self, words_lists):
    bag_of_words = defaultdict(int)

    for noun in iter_chain(*words_lists):
        if len(noun) > 1:
            bag_of_words[noun] += 1

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])

    return dict(top_words[-20:])
