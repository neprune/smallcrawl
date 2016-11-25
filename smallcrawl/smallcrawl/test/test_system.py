"""Tests that the generated asset list is as expected for certain sites.
Uses vcrpy to store and mock the HTTP requests for the sites.
"""
import pytest
import vcr

from .. import crawl
from .sites import TEST_SITES


@pytest.mark.parametrize('site', TEST_SITES)
def test_assets_match(site):
    with vcr.use_cassette(site.cassette):

        # sort both by urls
        def get_url(x):
            return x['url']

        found = list(crawl(page_url=site.url, domain=site.url))
        found = found.sort(key=get_url)
        expected = site.assets.sort(key=get_url)

        assert found == expected
