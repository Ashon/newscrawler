import re

from core.crawler import CrawlingTarget


class NaverNewsCrawlingTarget(CrawlingTarget):
    def get_content_wrapper(self, soup):
        return soup.find_all(**self._selector)[0]

    def filter_content(self, content):
        filter_tags = ['script', 'h4']
        for tag in filter_tags:
            unwanted = content.find(tag)
            if unwanted:
                unwanted.extract()

    def sanitize_content(self, content):
        article_text = re.sub(r'[\n,\t]', '', content.text)
        return article_text
