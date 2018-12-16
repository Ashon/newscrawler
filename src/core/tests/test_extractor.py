from core.extractor import PageExtractor


HTML_FIXTURE = '''
<html>
  <head>
    <title>test page</title>
  </head>
  <body>
    <div id="content">
      <span class="simple-text">this is simple text</span>
    </div>
  </body>
</html>
'''


def test_crawling_target(requests_mock):
    requests_mock.get('http://crawling-test.com/?page=1', text=HTML_FIXTURE)

    target = PageExtractor(
        url_pattern='http://crawling-test.com/?page={id}',
        selector={
            'name': 'span',
            'class': 'simple-text'
        }
    )

    extracted_text = target.extract(id=1)
    assert extracted_text[0].text == 'this is simple text'
