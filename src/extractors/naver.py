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
