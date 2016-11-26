# smallcrawl - A *Very* Basic Command-Line Web Crawler

A simple single-threaded web crawler that given a starting URL will visit every
reachable page under that domain.

At each page it determines the URLs of every static asset (images, javascript,
stylesheets).

It ouptuts this information in JSON format, listing the URLs of every
static asset, grouped by page.

## Example

```bash
> crawl http://www.example.org
[
  {
    "url": "http://www.example.org",
    "assets": [
      "http://www.example.org/image.jpg",
      "http://www.example.org/script.js"
    ]
  },
  {
    "url": "http://www.example.org/about",
    "assets": [
      "http://www.example.org/company_photo.jpg",
      "http://www.example.org/script.js"
    ]
  }
  ..
]
```

## Installation & Usage

Requires Python 3.3+ and [pip](https://pip.pypa.io/en/stable/installing/).

(Using a [virtualenv](https://virtualenv.pypa.io/en/stable/)
is recommended.)

Inside the smallcrawl directory, use pip to install smallcrawl
package:

```bash
pip install -e smallcrawl
```

Now you should be able to run the crawler like so:
```bash
> crawl <start url>
```

## A bit more detail...

Performs a DFS at the given starting page.

If a connection error or redirect occurs on the first URL, crawling is terminated
with an error message.

On other URLS, errors are silently ignored and valid redirects are followed.

## What's next?

Some things that might be interesting to work on:

* Parallel crawling

* Better management of 429 (too many requests) and similar responses - wait some
period of time before trying again

* Respect for robots.txt
