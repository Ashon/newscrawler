import re

from bs4 import BeautifulSoup as bs
import requests


class CrawlingTarget(object):
    def __init__(self, url_pattern, selector):
        self._url_pattern = url_pattern
        self._selector = selector

    def extract(self, **kwargs):
        url = self._url_pattern.format(**kwargs)

        res = requests.get(url)
        soup = bs(res.text, 'html.parser')

        # find root content tag
        article = self.get_content_wrapper(soup)

        # filter unwanted elements
        self.filter_content(article)

        # sanitize content text
        article_text = self.sanitize_content(article)

        return article_text

    def get_content_wrapper(self, soup):
        return soup.find_all(**self._selector)

    def filter_content(self, content):
        pass

    def sanitize_content(self, content):
        return content


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
