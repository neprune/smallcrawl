from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_page(page_contents, page_url=None):
    """Function for retrieving the links and static assets of a given webpage.
    Resolves relative links using the given page_url.

    Returns (links, assets), both as sets.

    Uses the slow but lenient html5lib as the back-end parser for bs4.
    lxml may be preferred for speed but requires an external c dependency.
    See docs for more detail:
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
    """

    # work around python's 'interesting' mutable defaults
    page_url = '' if page_url is None else page_url

    link_tags = ['a']
    asset_tags = ['img', 'script', 'link']

    # html5lib can only parse the whole page - no 'SoupStrainer' to filter by
    tags = BeautifulSoup(page_contents, 'html5lib')

    page_links = [tag.get('href') for tag in tags.find_all(link_tags)]

    def extract_asset_link(tag):
        """Returns the relavant link from a given asset tag.
        If the tag is not an asset, None is returned."""

        if tag.name == 'img' or tag.name == 'script':
            return tag.get('src')
        elif tag.name == 'link' and 'stylesheet' in tag.get('rel', []):
            return tag.get('href')
        else:
            return None

    asset_links = map(extract_asset_link, tags.find_all(asset_tags))

    def resolve_links(links):
        """Resolves all relative links and removes None's."""

        def resolve(link):
            """Resolve relative link, return None if invalid or same
            the as the URL."""
            resolved = urljoin(page_url, link)
            return resolved if resolved != page_url else None

        links = map(resolve, links)
        return filter(None.__ne__, links)  # remove None's

    return (set(resolve_links(page_links)), set(resolve_links(asset_links)))
