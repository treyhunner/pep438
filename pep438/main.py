"""Command-line interface for pep438 command"""
from __future__ import print_function, unicode_literals
import sys
from getopt import getopt, GetoptError

from clint import piped_in
from clint.textui import puts, columns, indent
from clint.textui.core import STDOUT, STDERR
from clint.textui.colored import green, red, blue

from . import __version__
from .core import get_links, get_pypi_packages


def version():
    print("pep438 version %s" % __version__)


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
    input_lines = None and piped_in()

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
