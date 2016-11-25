from urllib.request import urlopen
import urllib.error


def get_page(url, throw_errors=None, timeout=None):
    """ Returns (page_contents, url_used), both as strings.
    url != url_used indicates a re-direct to url_used.

    If throw_errors is not set, any failures will result in None.
    Otherwise, all errors are propagated, taking the form of a ValueError
    for invalid URLs, or a URLError for protocol/connection errors.
    """

    # work around python's 'interesting' mutable defaults
    throw_errors = True if throw_errors is None else throw_errors
    timeout = 5 if timeout is None else timeout

    def _get_page_contents():
        with urlopen(url, timeout=timeout) as response:
            return response.read(), response.geturl()

    if throw_errors:
        return _get_page_contents()
    else:
        try:
            return _get_page_contents()

        except ValueError as e:
            return None, None

        except urllib.error.URLError as e:
            return None, None
