"""Mocks crawler components to test the underlying crawl logic.
"""
import pytest

from .. import crawl


GET_PAGE_MOCK_PATH = 'smallcrawl.crawler.get_page'
PARSE_PAGE_MOCK_PATH = 'smallcrawl.crawler.parse_page'


def get_mocks(mocker):
    get_page_mock = mocker.patch(GET_PAGE_MOCK_PATH)
    parse_page_mock = mocker.patch(PARSE_PAGE_MOCK_PATH)
    return get_page_mock, parse_page_mock


def test_terminate_on_no_valid_links(mocker):
    start_url = 'http://test.com'
    get_page_mock, parse_page_mock = get_mocks(mocker)

    get_page_mock.return_value = ("", start_url)  # no content, no redirect

    assets = {'asset1', 'asset2'}
    parse_page_mock.return_value = (set(['http://not.test.com']), assets)

    crawl_iterator = crawl(page_url=start_url, domain=start_url)

    # check first run
    assets_dict = next(crawl_iterator)
    assert list(assets) == assets_dict['assets']
    assert start_url == assets_dict['url']

    # ensure we terminate here
    with pytest.raises(StopIteration):
        next(crawl_iterator)


def test_continue_on_valid_links(mocker):
    start_url = 'http://test.com'
    next_url = start_url + '/link'
    get_page_mock, parse_page_mock = get_mocks(mocker)

    get_page_mock.return_value = ("", start_url)  # no content, no redirect
    parse_page_mock.return_value = (set([next_url]), set())

    crawl_iterator = crawl(page_url=start_url, domain=start_url)

    # skip over first call
    next(crawl_iterator)

    get_page_mock.return_value = ("", next_url)  # no content, no redirect
    assets = {'asset1', 'asset2'}
    parse_page_mock.return_value = (set(), assets)

    assets_dict = next(crawl_iterator)
    assert list(assets) == assets_dict['assets']
    assert next_url == assets_dict['url']

    # ensure we terminate here
    with pytest.raises(StopIteration):
        next(crawl_iterator)


def test_doesnt_revisit_link(mocker):
    crawl_iterator = crawl(page_url='http://test.com/link',
                           domain='http://test.com',
                           visited=['http://test.com/link'])
    with pytest.raises(StopIteration):
        next(crawl_iterator)


def test_valid_redirect_on_first_throws_error(mocker):
    get_page_mock, parse_page_mock = get_mocks(mocker)
    get_page_mock.return_value = ('', 'http://test.com/otherlink')

    crawl_iterator = crawl(page_url='http://test.com/link',
                           domain='http://test.com')

    with pytest.raises(OSError):
        next(crawl_iterator)


def test_invalid_redirect_is_ignored_after_first_run(mocker):
    get_page_mock, parse_page_mock = get_mocks(mocker)
    get_page_mock.return_value = ('', 'http://redirect.com')
    parse_page_mock.return_value = (set(), set())

    crawl_iterator = crawl(page_url='http://test.com/link',
                           domain='http://test.com',
                           first_run=False)

    with pytest.raises(StopIteration):
        next(crawl_iterator)


def test_invalid_redirect_is_pursued_after_first_run(mocker):
    redirect_url = 'http://test.com/otherlink'
    get_page_mock, parse_page_mock = get_mocks(mocker)
    get_page_mock.return_value = ('', redirect_url)
    parse_page_mock.return_value = (set(), set())

    crawl_iterator = crawl(page_url='http://test.com/link',
                           domain='http://test.com',
                           first_run=False)

    asset_dict = next(crawl_iterator)
    assert asset_dict['url'] == redirect_url
    assert asset_dict['assets'] == []

    with pytest.raises(StopIteration):
        next(crawl_iterator)


def test_get_page_errors_propogated_on_first_run(mocker):
    # TODO: check ValueError and OSError are propogated
    pass


def test_get_page_errors_ignored_after_first_run(mocker):
    # TODO: check ValueError and OSError are not propogated
    pass


def test_general_error_propogated_after_first_run(mocker):
    # TODO: check Exception is propogated
    pass
