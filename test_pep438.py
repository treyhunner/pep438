#!/usr/bin/env python
import unittest
import sys
from io import StringIO

from clint.textui import core
import pep438


class patch_io(object):

    streams = ('stdout', 'stdin', 'stderr')

    def __init__(self):
        for stream in self.streams:
            setattr(self, stream, StringIO())
            setattr(self, 'real_%s' % stream, getattr(sys, stream))
        self.real_STDOUT = core.STDOUT
        self.real_STDERR = core.STDERR

    def __enter__(self):
        for stream in self.streams:
            setattr(sys, stream, getattr(self, stream))
        self.STDOUT = self.stdout.write
        self.STDERR = self.stderr.write
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for stream in self.streams:
            getattr(sys, stream).close()
            setattr(sys, stream, getattr(self, 'real_%s' % stream))
        core.STDOUT = self.real_STDOUT
        core.STDERR = self.real_STDERR


class CommandLineTests(unittest.TestCase):

    def test_version(self):
        for args in (['pep438', '-v'], ['pep438', '--version']):
            with patch_io() as new:
                sys.argv = args
                self.assertRaises(SystemExit, pep438.main)
                self.assertEqual(new.stdout.getvalue(), "0.1.0\n")


if __name__ == '__main__':
    unittest.main()
