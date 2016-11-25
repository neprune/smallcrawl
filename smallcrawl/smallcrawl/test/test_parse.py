"""Unit tests the parser on a variety of pages."""
from .pages import TEST_PAGES
from ..parse import parse_page

import pytest


@pytest.mark.parametrize('page', TEST_PAGES)
def test_parse_assets(page):
    links, assets = parse_page(page.text, page_url=page.url)
    assert assets == page.unique_assets


@pytest.mark.parametrize('page', TEST_PAGES)
def test_parse_links(page):
    links, assets = parse_page(page.text, page_url=page.url)
    assert links == page.unique_urls
