import time
from collections import defaultdict
from datetime import datetime
import itertools

import mecab

from core.crawler import CrawlingTarget
from crawlers import NaverNewsCrawlingTarget

import settings


MAX_PAGES_PER_DATE = 5


def harvest(today):
    naver_news_list = CrawlingTarget(
        **settings.SPIDER_CONFIG['naver']['news_list'])

    naver_news = NaverNewsCrawlingTarget(
        **settings.SPIDER_CONFIG['naver']['news_page'])

    for i in range(MAX_PAGES_PER_DATE):
        news_links = naver_news_list.extract(date=today, page=i)
        for link in news_links:
            article_text = naver_news.extract(link=link['href'])
            yield article_text


def main():
    today = datetime.now().strftime('%Y%m%d')
    iter_articles = harvest(today)

    m = mecab.MeCab()
    nouns = itertools.chain(*(m.nouns(article) for article in iter_articles))

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
