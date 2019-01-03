from extractors.naver import NaverNewsContentExtractor


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
