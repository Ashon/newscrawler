import asyncio
import functools
import itertools
import time

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

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


async def harvest(loop, pool, date, page):
    news_links = link_extractor.extract(date=date, page=page)

    return await asyncio.gather(*(
        loop.run_in_executor(pool, functools.partial(
            content_extractor.extract, link=link['href']))
        for link in news_links
    ))


async def main(loop):
    pool = ProcessPoolExecutor(settings.PROCESSES)

    today = datetime.now().strftime('%Y%m%d')

    articles = itertools.chain(*[
        await harvest(loop, pool, today, page)
        for page in range(settings.MAX_PAGES_PER_DATE)
    ])

    m = mecab.MeCab()
    nouns = itertools.chain(*(m.nouns(article) for article in articles))

    bag_of_words = defaultdict(int)
    for noun in nouns:
        bag_of_words[noun] += 1
    print(bag_of_words)

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])
    print(top_words[-20:])


if __name__ == '__main__':
    start = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

    duration = time.time() - start
    print(duration)
