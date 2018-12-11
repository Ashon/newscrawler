from crawler import CrawlingTarget
from crawler import NaverNewsCrawlingTarget


def main():
    naver_news_list = CrawlingTarget(
        url_pattern=(
            'https://news.naver.com/main/list.nhn'
            '?mode=LSD&sid1=001&mid=sec&listType=title'
            '&date={date}&page={page}'
        ),
        selector={
            'class': 'nclicks(fls.list)'
        }
    )

    naver_news = NaverNewsCrawlingTarget(
        url_pattern='{link}',
        selector={
            'name': 'div',
            'id': 'articleBodyContents'
        }
    )

    news_links = naver_news_list.extract(date='20181211', page=1)
    for link in news_links:
        article_text = naver_news.extract(link=link['href'])

        print(link.text)
        print(article_text)
        print('*' * 100)


if __name__ == '__main__':
    main()
