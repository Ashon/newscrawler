import re
from datetime import datetime

from extractors.naver import NaverNewsLinkExtractor
from extractors.naver import NaverNewsContentExtractor
from extractors.naver import load_extractor


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


def test_content_extractor():
    content_extractor = NaverNewsContentExtractor(
        url_pattern='{link}',
        selectors={
            'content': {
                'name': 'div',
                'id': 'articleBodyContents'
            },
            'date': {
                'name': 'span',
                'class': 't11'
            }
        }
    )

    url = (
        'https://news.naver.com/main/read.nhn?'
        'mode=LSD&mid=sec&sid1=001&oid=030&aid=0002772003'
    )

    content = content_extractor.extract(link=url)

    assert type(content) is dict
    assert 'date' in content
    assert 'content' in content


def test_naver_extrator_loader():
    link, content = load_extractor()

    assert link is not None
    assert content is not None

    today = datetime.now().strftime('%Y%m%d')
    extracted_links = link.extract(date=today, sid='001', page=1)

    assert type(extracted_links['links']) is list
    assert type(extracted_links['links'][0]) is dict
    assert 'text' in extracted_links['links'][0]
    assert 'url' in extracted_links['links'][0]

    extracted_content = content.extract(
        link=extracted_links['links'][0]['url'])

    assert type(extracted_content) is dict
    assert 'date' in extracted_content
    assert 'content' in extracted_content
