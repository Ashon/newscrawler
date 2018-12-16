import re

from core.crawler import CrawlingTarget


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


class NaverNewsCrawlingTarget(CrawlingTarget):
    def get_content_wrapper(self, soup):
        content = soup.find_all(**self._selector)[0]

        return content

    def filter_content(self, content):
        for tag in FILTER_TAGS:
            unwanted = content.find(tag)
            if unwanted:
                unwanted.extract()

    def sanitize_content(self, content):
        article_text = re.sub(
            f'[{",".join(FILTER_TEXT_PATTERNS)}]', '',
            content.text)
        return article_text
