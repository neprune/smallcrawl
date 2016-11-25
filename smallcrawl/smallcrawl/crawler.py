from .parse import parse_page
from .get_page import get_page


def crawl(page_url, domain, visited=None, first_run=None):
    """Returns an iterator for a DFS starting at the given page, filtering by
    pages starting under the given domain.

    The iterator provides the static assets available at each page as:
    {'url' : <url of page>, 'assets' : <list of static assets>}

    On the first run, errors in retreiving the page are raised.
    This can be a ValueError to indicate the given url is invalid, or an
    OSError to indicate getting the page failed.
    Additionally, a re-direct is treated like an OSError.

    On other runs, errors are silently ignored and re-directs are followed
    if they lead to a URL that is under the given domain.
    """

    # work around python's 'interesting' mutable defaults
    visited = [] if visited is None else visited
    first_run = True if first_run is None else first_run

    if page_url not in visited:
        visited.append(page_url)

        # get the page, only allowing errors if it's our first run
        page_contents, url_used = get_page(page_url, throw_errors=first_run)

        # ignore this url if getting the page failed
        if page_contents is None:
            return

        # redirected
        if (url_used != page_url):

            # treat a redirect as an error on our first run
            if first_run:
                err = 'Re-direct on first url ' + page_url + ' to ' + url_used
                raise OSError(err)

            # continue if redirected to a valid url we haven't visited
            elif url_used.startswith(domain) and url_used not in visited:
                visited.append(url_used)
                page_url = url_used

            # otherwise, silently ignore
            else:
                return

        links, assets = parse_page(page_contents, page_url)
        links = filter(lambda l: l.startswith(domain), links)

        # remove the end of fragment identifiers - don't want to revisit pages
        links = map(lambda l: l.split('#', 1)[0], links)

        yield {'url': page_url, 'assets': list(assets)}

        for link in links:
            yield from crawl(page_url=link,
                             domain=domain,
                             visited=visited,
                             first_run=False)
