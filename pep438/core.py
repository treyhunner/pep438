"""Core pep438 utility functions"""
from __future__ import unicode_literals

import requests
import lxml.html
from reqfileparser import parse


def get_links(package_name):
    """Return list of links on package's PyPI page"""
    response = requests.get('https://pypi.python.org/simple/%s' % package_name)
    response.raise_for_status()
    page = lxml.html.fromstring(response.content)
    external_links = [link for link in page.xpath('//a')
                      if not link.get('href').startswith('../')]
    return external_links


def get_pypi_packages(fileobj):
    """Return all PyPI-hosted packages from file-like object"""
    return [p['name'] for p in parse(fileobj) if not p.get('uri')]
