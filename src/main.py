import time
from collections import defaultdict
from datetime import datetime
import itertools
import multiprocessing

import mecab

from core.crawler import CrawlingTarget
from crawlers import NaverNewsCrawlingTarget

import settings


MAX_PAGES_PER_DATE = 30


manager = multiprocessing.Manager()

naver_news_list = CrawlingTarget(
    **settings.SPIDER_CONFIG['naver']['news_list'])

naver_news = NaverNewsCrawlingTarget(
    **settings.SPIDER_CONFIG['naver']['news_page'])


def extract_content(link):
    return naver_news.extract(link=link)


def harvest(today, page):
    news_links = naver_news_list.extract(date=today, page=page)
    pool = multiprocessing.Pool(8)
    articles = pool.map(
        extract_content, [link['href'] for link in news_links]
    )

    return articles


def main():
    today = datetime.now().strftime('%Y%m%d')

    iter_articles = itertools.chain(*(
        harvest(today, i) for i in range(MAX_PAGES_PER_DATE)
    ))

    m = mecab.MeCab()
    nouns = itertools.chain(*(
        m.nouns(article) for article in iter_articles
    ))

    bag_of_words = defaultdict(int)
    for noun in nouns:
        bag_of_words[noun] += 1
    print(bag_of_words)

    top_words = sorted(bag_of_words.items(), key=lambda x: x[1])
    print(top_words[-20:])


if __name__ == '__main__':
    start = time.time()

    main()

    duration = time.time() - start
    print(duration)
