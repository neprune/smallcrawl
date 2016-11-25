"""Provides a list of TestPages that group a pages content with it's contained
assets and links to test against.
"""
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep
PAGES_DIR = SCRIPT_DIR + 'fixtures' + os.sep + 'pages' + os.sep


class TestPage(object):

    def __init__(self, page_name, url, unique_urls, unique_assets):
        self.url = url
        self.name = page_name
        self.text = self.read_contents(page_name)
        self.unique_urls = unique_urls
        self.unique_assets = unique_assets

    @staticmethod
    def read_contents(page_name):
        with open(PAGES_DIR + page_name, 'r') as f:
            return f.read()


TEST_PAGES = (
    TestPage('empty.html',
             url='',
             unique_urls=set(),
             unique_assets=set()),

    TestPage('blank.html',
             url='',
             unique_urls=set(),
             unique_assets=set()),

    TestPage('links_basic.html',
             url='',
             unique_urls={'link1', 'link2'},
             unique_assets=set()),

    TestPage('images_basic.html',
             url='',
             unique_urls=set(),
             unique_assets={'image1', 'image2'}),

    TestPage('scripts_basic.html',
             url='',
             unique_urls=set(),
             unique_assets={'script1', 'script2'}),

    TestPage('stylesheets_basic.html',
             url='',
             unique_urls=set(),
             unique_assets={'stylesheet1', 'stylesheet2'}),

    TestPage('stylesheets_incorrect_relation.html',
             url='',
             unique_urls=set(),
             unique_assets={'stylesheet1'}),

    TestPage('relative_and_absolute_links.html',
             url='http://test.com/a/b/',
             unique_urls={'http://link', 'http://test.com/a/b/link',
                          'http://test.com/a/link', 'http://test.com/link'},
             unique_assets={'http://stylesheet',
                            'http://test.com/a/b/stylesheet',
                            'http://test.com/a/stylesheet',
                            'http://test.com/stylesheet',
                            'http://image', 'http://test.com/a/b/image',
                            'http://test.com/a/image',
                            'http://test.com/image',
                            'http://script', 'http://test.com/a/b/script',
                            'http://test.com/a/script',
                            'http://test.com/script'}),
)
