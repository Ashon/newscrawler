import re

from core.extractor import PageExtractor


FILTER_TEXT_PATTERNS = [
    '\n',
    '\t',
    '▶.*',
    'ⓒ.*',
]

FILTER_TAGS = [
    'script',
    'h4',
    'span',
    'a',
    'strong'
]


NEWS_LIST_URL_PATTERN = (
    'https://news.naver.com/main/list.nhn'
    '?mode=LSD&sid1={sid}&mid=sec&listType=title'
    '&date={date}&page={page}'
)
NEWS_LIST_SELECTOR = {
    'links': {
        'name': 'a',
        'class_': re.compile(
            r'nclicks\((%s)\)' % '|'.join((
                'fls.list', 'cls_pol.clsart', 'cls_eco.clsart',
                'cls_nav.clsart', 'cls_lif.clsart', 'cls_wor.clsart',
                'cls_sci.clsart'
            ))
        )
    }
}

NEWS_CONTENT_URL_PATTERN = '{link}'
NEWS_CONTENT_SELECTOR = {
    'content': {
        'name': 'div',
        'id': 'articleBodyContents'
    },
    'date': {
        'name': 'span',
        'class': 't11'
    }
}


class NaverNewsLinkExtractor(PageExtractor):
    def get_content_wrapper(self, soup):
        content = super(NaverNewsLinkExtractor, self).get_content_wrapper(soup)
        for key, value in content.items():
            content[key] = [{
                'text': link.text,
                'url': link['href']
            } for link in value]

        return content


class NaverNewsContentExtractor(PageExtractor):
    def get_content_wrapper(self, soup):
        content = super(NaverNewsContentExtractor, self).get_content_wrapper(soup)

        for key, value in content.items():
            content[key] = value[0]

        return content

    def filter_content(self, results):
        for key, value in results.items():
            for tag in FILTER_TAGS:
                unwanted = value.find(tag)
                if unwanted:
                    unwanted.extract()

    def sanitize_content(self, results):
        for key, value in results.items():
            results[key] = re.sub(
                f'[{",".join(FILTER_TEXT_PATTERNS)}]', '',
                value.text)

        return results


def load_extractor():
    link_extractor = NaverNewsLinkExtractor(
        url_pattern=NEWS_LIST_URL_PATTERN,
        selectors=NEWS_LIST_SELECTOR)

    content_extractor = NaverNewsContentExtractor(
        url_pattern=NEWS_CONTENT_URL_PATTERN,
        selectors=NEWS_CONTENT_SELECTOR)

    return link_extractor, content_extractor
