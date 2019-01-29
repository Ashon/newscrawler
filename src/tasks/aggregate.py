from collections import defaultdict
from itertools import chain

from celery import Task


class Aggregate(Task):
    name = 'aggregate'

    def run(self, words_lists):
        bag_of_words = defaultdict(int)

        for noun in chain(*words_lists):
            if len(noun) > 1:
                bag_of_words[noun] += 1

        top_words = sorted(bag_of_words.items(), key=lambda x: x[1])

        return dict(top_words[-20:])
