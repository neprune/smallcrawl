"""Defines command line usage of the package."""
from smallcrawl import crawl

import json
import sys
import textwrap


def print_crawl_as_json_list(start_url):
    """Prints the assets groups as a single JSON list.

    Iterate through the crawl function, printing as we go so we don't appear
    to hang on large websites.
    """

    def format_assets_dict(assets_dict, indent):
        """Return JSON for the given dict using the given indentation level
        inside the JSON, and on the whole thing.
        """
        json_string = json.dumps(
                assets_dict, indent=indent, separators=(',', ': '))
        return textwrap.indent(json_string, indent * ' ')

    # NOTE: trailing commas are not allowed in JSON, hence awkward printing

    crawl_iterator = crawl(page_url=start_url, domain=start_url)
    indent = 2

    print('[', end='')

    # ugly way of safely getting the first item
    for assets_dict in crawl_iterator:
        print('\n' + format_assets_dict(assets_dict, indent=indent), end='')
        break

    for assets_dict in crawl_iterator:
        print(',\n' + format_assets_dict(assets_dict, indent=indent), end='')

    print('\n]')


def main():
    """Entry point for the command-line call."""

    if len(sys.argv) != 2:
        print('Requires a single starting url.')
        sys.exit(1)

    start_url = sys.argv[1]

    try:
        print_crawl_as_json_list(start_url)
        sys.exit(0)

    except (OSError, ValueError) as e:
        print('ABORTING: ' + str(e))
        sys.exit(1)
