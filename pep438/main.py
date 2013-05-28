"""Command-line interface for pep438 command"""
from __future__ import print_function, unicode_literals
import sys
from getopt import getopt, GetoptError

from clint import piped_in
from clint.textui import puts, columns, indent
from clint.textui.core import STDOUT, STDERR
from clint.textui.colored import green, red, blue

from . import __version__
from .core import (get_links, get_pypi_packages, valid_package,
                   get_pypi_user_packages)


def version():
    print("pep438 version %s" % __version__)


def usage(error=False):
    """Print usage information and if error is ``True`` print to stderr"""
    out = STDERR if error else STDOUT
    options = [
        ("-h, --help", "Print this help message"),
        ("-v, --version", "Display version information"),
        ("-e, --errors-only", "Display errors only"),
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
        if option == '-u':
            packages += get_pypi_user_packages(arg)

    return packages


def get_packages_from_stdin():
    """Return packages found from standard input"""
    input_lines = piped_in()
    if input_lines is not None:
        return get_pypi_packages(input_lines)
    else:
        return []


def main():

    packages = []
    args = sys.argv[1:]

    try:
        opts, pkgs = getopt(args, "vhr:u:e", ["version", "help", "requirement",
                                              "user", "errors-only"])
    except GetoptError as e:
        puts(str(e), stream=STDERR)
        usage(error=True)
        sys.exit(2)

    packages += pkgs
    packages += process_options(opts)
    packages += get_packages_from_stdin()
    show_only_errors = ('-e', '') in opts or ('--errors-only', '') in opts

    if not packages:
        # Return error if no packages found
        usage(error=True)
        sys.exit(2)

    for package in packages:
        if valid_package(package):
            links = get_links(package)
            symbol = red('\u2717') if links else green('\u2713')
            msg = "%s %s: %s links" % (symbol, blue(package), len(links))
            if links or not show_only_errors:
                print(msg)
        else:
            print("%s %s: not found on PyPI" % (red('\u26a0'), blue(package)),
                  file=sys.stderr)
