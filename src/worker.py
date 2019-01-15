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


def serialize_extractor_kwargs(args, kwargs):
    """Returns extractor kwargs dict

    Params
        args: tuple which has item type is dict.
        kwargs: dict object which key is item's key in args,
                each value has 'key', 'value' for references of args item.

    Example
        >>> args = ({'id': 1, 'name': 'foo'}, )
        >>> kwargs = {'changed_name': {'key': 'name'}}
        >>> r = serialize_extractor_kwargs(args, kwargs)
        >>> r == {'changed_name': 'foo'}
    """

    if len(args) == 0:
            args = ({},)

    resolved_extractor_kwargs = {}
    for k, v in kwargs.items():
        value = v.get('value', args[0].get(v.get('key')))
        resolved_extractor_kwargs[k] = value

    return resolved_extractor_kwargs


@app.task(bind=True)
def harvest(self, *args, harvester, harvester_type, **kwargs):
    harvester = current_app.extractors[harvester][harvester_type]

    try:
        extractor_kwargs = serialize_extractor_kwargs(args, kwargs)
        news_content = harvester.extract(**extractor_kwargs)

        return news_content

    except Exception as exc:
        # Celery Issues: 4222
        self.update_state(state=states.FAILURE)
        return {'exc': str(exc)}


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
