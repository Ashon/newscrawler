import asyncio

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import partial
from itertools import chain
from time import time

import mecab
import uvloop

from core.extractor import PageExtractor
from extractors import NaverNewsPageExtractor

import settings


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

link_extractor = PageExtractor(
    **settings.SPIDER_CONFIG['naver']['news_list'])

content_extractor = NaverNewsPageExtractor(
    **settings.SPIDER_CONFIG['naver']['news_page'])


async def harvest_content(loop, pool, news_links):
    return await asyncio.gather(*(
        loop.run_in_executor(pool, partial(
            content_extractor.extract, link=link['href']))
        for link in news_links
    ))


async def main(loop, pool):
    today = datetime.now().strftime('%Y%m%d')

    articles = chain(*[
        await harvest_content(
            loop, pool, link_extractor.extract(date=today, page=page)
        ) for page in range(settings.MAX_PAGES_PER_DATE)
    ])

    m = mecab.MeCab()
    nouns = chain(*(
        m.nouns(article) for article in articles
    ))

    bag_of_words = defaultdict(int)
    for noun in nouns:
        bag_of_words[noun] += 1
    print(bag_of_words)

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])
    print(top_words[-20:])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pool = ProcessPoolExecutor(settings.PROCESSES)

    start = time()
    loop.run_until_complete(main(loop, pool))
    duration = time() - start
    print(duration)
