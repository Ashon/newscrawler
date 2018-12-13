SPIDER_CONFIG = {
    'naver': {
        'news_list': {
            'url_pattern': (
                'https://news.naver.com/main/list.nhn'
                '?mode=LSD&sid1=001&mid=sec&listType=title'
                '&date={date}&page={page}'),
            'selector': {
                'class': 'nclicks(fls.list)'
            }
        },
        'news_page': {
            'url_pattern': '{link}',
            'selector': {
                'name': 'div',
                'id': 'articleBodyContents'
            }
        }
    }
}
