"""Holds a list of test sites including their expected assets list to test
against, and the corresponding vrcpy casettes so we don't have to rely on the
site not changing and a working connection to test against.
"""
import os
import json


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep
SITES_DIR = SCRIPT_DIR + 'fixtures' + os.sep + 'sites' + os.sep
CASSETTES_DIR = SITES_DIR + 'vcr_cassettes' + os.sep
ASSETS_DIR = SITES_DIR + 'assets' + os.sep


class TestSite(object):

    def __init__(self, protocol, address, comment):
        self.url = protocol + address

        address = address.replace('/', '_')
        self.cassette = CASSETTES_DIR + address + '.yaml'
        self.assets = self.load_json(ASSETS_DIR + address + '.json')
        self.comment = comment

    @staticmethod
    def load_json(json_file):
        with open(json_file, 'r') as f:
            return json.loads(f.read())


TEST_SITES = (
    TestSite('http://', 'nikgupta.uk',
         comment='Small static site.'),
    TestSite('http://', 'vcrpy.readthedocs.io/en/latest/',
         comment='Small static site.'),
    TestSite('https://', 'en.wikipedia.org/wiki/Web_crawler',
         comment='Small site with many frag identifiers to be ignored.'),
)
