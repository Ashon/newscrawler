import re
from datetime import datetime

from extractors.naver import NaverNewsLinkExtractor


def test_link_extractor():
    link_extractor = NaverNewsLinkExtractor(
        url_pattern=(
            'https://news.naver.com/main/list.nhn'
            '?mode=LSD&sid1={sid}&mid=sec&listType=title'
            '&date={date}&page={page}'
        ),
        selectors={
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
    )

    today = datetime.now().strftime('%Y%m%d')
    links = link_extractor.extract(date=today, sid='001', page=1)

    assert type(links['links']) is list
    assert type(links['links'][0]) is dict
    assert 'text' in links['links'][0]
    assert 'url' in links['links'][0]
