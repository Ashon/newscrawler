from crawler import CrawlingTarget
from crawler import NaverNewsCrawlingTarget

import settings


def main():
    naver_news_list = CrawlingTarget(
        **settings.SPIDER_CONFIG['naver']['news_list'])

    naver_news = NaverNewsCrawlingTarget(
        **settings.SPIDER_CONFIG['naver']['news_page'])

    news_links = naver_news_list.extract(date='20181211', page=1)
    for link in news_links:
        article_text = naver_news.extract(link=link['href'])

        print(link.text)
        print(article_text)
        print('*' * 100)


if __name__ == '__main__':
    main()
