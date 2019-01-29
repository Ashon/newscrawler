import mecab
from celery import Task


m = mecab.MeCab()


class Extract(Task):
    name = 'extract'

    def run(self, extracted_content, *args, method):
        fn = getattr(m, method)
        nouns = fn(extracted_content['content'])

        return nouns
