import os
import re

env = os.environ


BROKER_URL = env.get('BROKER_URL')
BACKEND_URL = env.get('BACKEND_URL')

SPIDER_CONFIG = {
    'naver': {
        'news_list': {
            'url_pattern': (
                'https://news.naver.com/main/list.nhn'
                '?mode=LSD&sid1={sid}&mid=sec&listType=title'
                '&date={date}&page={page}'
            ),
            'selectors': {
                'links': {
                    'name': 'a',
                    'class_': re.compile(
                        r'nclicks\((%s)\)' % '|'.join((
                            'fls.list',
                            'cls_pol.clsart',
                            'cls_eco.clsart',
                            'cls_nav.clsart',
                            'cls_lif.clsart',
                            'cls_wor.clsart',
                            'cls_sci.clsart',
                        ))
                    )
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
