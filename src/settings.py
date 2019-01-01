import os

env = os.environ


BROKER_URL = env.get('BROKER_URL')
BACKEND_URL = env.get('BACKEND_URL')

SPIDER_CONFIG = {
    'naver': {
        'news_list': {
            'url_pattern': (
                'https://news.naver.com/main/list.nhn'
                '?mode=LSD&sid1=001&mid=sec&listType=title'
                '&date={date}&page={page}'
            ),
            'selectors': {
                'links': {
                    'class': 'nclicks(fls.list)'
                }
            }
        },
        'news_page': {
            'url_pattern': '{link}',
            'selectors': {
                'content': {
                    'name': 'div',
                    'id': 'articleBodyContents'
                },
                'date': {
                    'name': 'span',
                    'class': 't11'
                }
            }
        }
    }
}
