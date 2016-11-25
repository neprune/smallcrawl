from setuptools import setup, find_packages

import sys


# using hex code since version tuple is inconsistent across versions
if sys.hexversion < 0x03030000:
    sys.exit('Sorry, only Python 3.3+ is supported')


setup(name='smallcrawl',
      version='0.1',
      description='A basic web crawler retrieving the urls of static assets.',
      author='Nik Gupta',
      author_email='vngupta77@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'beautifulsoup4==4.5.1',
          'html5lib==0.999999999',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'pytest-mock', 'vcrpy'],
      entry_points={
          'console_scripts': ['crawl=smallcrawl.command_line:main'],
      },
      zip_safe=False)
