"""Core pep438 utility functions"""
from __future__ import unicode_literals

import requests
import xmlrpclib
import lxml.html
from reqfileparser import parse


def valid_package(package_name):
    """Return bool if package_name is a valid package on PyPI"""
    response = requests.head('https://pypi.python.org/pypi/%s' % package_name)
    if response.status_code != 404:
        response.raise_for_status()
    return response.status_code != 404


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


def get_pypi_user_packages(user):
    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    return [x[1] for x in client.user_packages(user)]
