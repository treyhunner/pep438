#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import sys
from getopt import getopt, GetoptError

import requests
import lxml.html
from clint import piped_in
from clint.textui import puts, columns, indent
from clint.textui.core import STDOUT, STDERR
from clint.textui.colored import green, red, blue
from reqfileparser import parse


def get_links(package_name):
    """Return list of links on package's PyPI page"""
    response = requests.get('https://pypi.python.org/simple/%s' % package_name)
    page = lxml.html.fromstring(response.content)
    external_links = [link for link in page.xpath('//a')
                      if not link.get('href').startswith('../')]
    return external_links


def get_pypi_packages(fileobj):
    """Return all PyPI-hosted packages from file-like object"""
    return [p['name'] for p in parse(fileobj) if not p.get('uri')]


def version():
    print('0.1.0')  # TODO Abstract this out


def usage(error=False):
    """Print usage information and if error is ``True`` print to stderr"""
    out = STDERR if error else STDOUT
    options = [
        ("-h, --help", "Print this help message"),
        ("-v, --version", "Display version information"),
    ]

    puts("\nUsage:")
    with indent(4):
        puts("pep438 [options] <package name> ...", stream=out)
        puts("pep438 [options] -r <requirements file> ...", stream=out)
        puts("cat <requirements file> | pep438 [options]", stream=out)

    puts("\nAdditional Options:")
    with indent(4):
        max_len = max(len(option) for option, _ in options)
        for option, description in options:
            puts(columns([option, max_len + 5], [description, 99]), stream=out)


def process_options(options):
    """Returns given package names or prints help, version, or usage info"""
    packages = []
    for option, arg in options:
        if option in ('-h', '--help'):
            usage()
            sys.exit()
        if option in ('-v', '--version'):
            version()
            sys.exit()
        if option == '-r':
            with open(arg) as f:
                packages += get_pypi_packages(f)
    return packages


def main():

    packages = []
    args = sys.argv[1:]
    input_lines = piped_in()

    try:
        opts, pkgs = getopt(args, "vhr:", ["version", "help", "requirement"])
    except GetoptError as e:
        puts(str(e), stream=STDERR)
        usage(error=True)
        sys.exit(2)

    packages += pkgs
    packages += process_options(opts)

    if input_lines is not None:
        # Add packages found from standard input
        packages += get_pypi_packages(input_lines)
    elif not args:
        # Return error if no arguments given
        usage(error=True)
        sys.exit(2)

    for package in packages:
        links = get_links(package)
        symbol = red('\u2717') if links else green('\u2713')
        print("%s %s: %s links" % (symbol, blue(package), len(links)))


if __name__ == "__main__":
    main()
