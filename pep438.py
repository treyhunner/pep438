#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import requests
import lxml.html
from clint.textui.colored import green, red, blue
from reqfileparser import parse


def get_links(package_name):
    response = requests.get('https://pypi.python.org/simple/%s' % package_name)
    page = lxml.html.fromstring(response.content)
    external_links = [link for link in page.xpath('//a')
                      if not link.get('href').startswith('../')]
    return external_links


def get_links_from_file(filename):
    with open(filename, 'rb') as f:
        return ((p['name'], get_links(p['name'])) for p in parse(f))


def main():
    for name, links in get_links_from_file('requirements.txt'):
        symbol = red('\u2717') if links else green('\u2713')
        print("%s %s: %s external links" % (symbol, blue(name), len(links)))


if __name__ == "__main__":
    main()
