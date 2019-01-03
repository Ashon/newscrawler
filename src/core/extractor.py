from bs4 import BeautifulSoup as bs
import requests


class PageExtractor(object):
    def __init__(self, url_pattern, selectors):
        self._url_pattern = url_pattern
        self._selectors = selectors

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
        results = {
            key: soup.find_all(**selector)
            for key, selector in self._selectors.items()
        }

        return results

    def filter_content(self, results):
        pass

    def sanitize_content(self, results):
        return results
