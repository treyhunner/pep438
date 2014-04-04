#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
import sys
from io import StringIO

from mock import Mock, patch

from clint.textui import core
from pep438 import __version__
from pep438.main import main
from pep438.core import get_urls, get_pypi_packages


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


class TestValidPackage(unittest.TestCase):

    def test_valid_package_200(self):
        from pep438.core import valid_package
        config = {'return_value': Mock(status_code=200)}
        with patch('pep438.core.requests.head', **config):
            self.assertTrue(valid_package('dummy_package'))

    def test_not_valid_package_404(self):
        from pep438.core import valid_package
        config = {'return_value': Mock(status_code=404)}
        with patch('pep438.core.requests.head', **config):
            self.assertFalse(valid_package('dummy_package'))

    def test_valid_package_raises_HTTPError(self):
        from requests import HTTPError
        from pep438.core import valid_package
        response = Mock(status_code=500)
        response.raise_for_status = Mock(side_effect=HTTPError())
        config = {'return_value': response}
        with patch('pep438.core.requests.head', **config):
            self.assertRaises(HTTPError, valid_package, 'dummy_package')


class TestGetURLs(unittest.TestCase):

    def get_link(self, href, rel=None):
        if rel:
            return '<a href="%s" rel="%s">link text</a>' % (href, rel)
        else:
            return '<a href="%s">link text</a>' % href

    def get_response(self, *links):
        response = Mock(status_code=200)
        response.content = '<html>%s</html>' % ''.join(
            self.get_link(*d) for d in links)
        return response

    @patch('pep438.core.requests.get')
    def test_download_link(self, get):
        get.side_effect = lambda *args: self.get_response(
            ['test', "download"], ['../'])
        self.assertEqual(get_urls('package'), {'test'})

    @patch('pep438.core.requests.get')
    def test_homepage_link(self, get):
        get.side_effect = lambda *args: self.get_response(
            ['test', "homepage"], ['../'])
        self.assertEqual(get_urls('package'), {'test'})

    @patch('pep438.core.requests.get')
    def test_duplicate_urls(self, get):
        get.side_effect = lambda *args: self.get_response(
            ['test', "homepage"], ['../'], ['test', "download"])
        self.assertEqual(get_urls('package'), {'test'})

    @patch('pep438.core.requests.get')
    def test_wrong_rel(self, get):
        get.side_effect = lambda *args: self.get_response(
            ['test', "internal"], ['../'], ['test'])
        self.assertEqual(get_urls('package'), set([]))


class TestGetPyPIPackages(unittest.TestCase):

    def test_with_version(self):
        f = StringIO()
        f.write('Django==1.4.5')
        f.seek(0)
        self.assertEqual(get_pypi_packages(f), ['Django'])

    def test_no_version(self):
        f = StringIO()
        f.write('Django')
        f.seek(0)
        self.assertEqual(get_pypi_packages(f), ['Django'])

    def test_url(self):
        f = StringIO()
        f.write('https://github.com/django/django/archive/master.zip')
        f.seek(0)
        self.assertEqual(get_pypi_packages(f), [])


class CommandLineTests(unittest.TestCase):

    def setUp(self):
        get_urls_patcher = patch('pep438.main.get_urls')
        self.get_urls = get_urls_patcher.start()
        self.addCleanup(get_urls_patcher.stop)
        valid_package_patcher = patch('pep438.main.valid_package')
        self.valid_package = valid_package_patcher.start()
        self.addCleanup(valid_package_patcher.stop)
        self.valid_package.side_effect = lambda p: True
        self.get_urls.side_effect = lambda p: []

    def test_valid_package(self):
        sys.argv = ['pep438', 'p1', 'p2']
        with patch_io() as new:
            main()
            self.assertEqual(self.valid_package.call_count, 2)
            self.assertEqual(self.get_urls.call_count, 2)
            self.assertEqual(new.stderr.getvalue(), "")
            self.assertEqual(new.stdout.getvalue(),
                             "\u2713 p1: 0 URLs\n\u2713 p2: 0 URLs\n")

    def test_stdin(self):
        sys.argv = ['pep438']
        with patch_io() as new:
            new.stdin.write('p1\np2\n')
            new.stdin.seek(0)
            main()
            self.assertEqual(self.valid_package.call_count, 2)
            self.assertEqual(self.get_urls.call_count, 2)
            self.assertEqual(new.stderr.getvalue(), "")
            self.assertEqual(new.stdout.getvalue(),
                             "\u2713 p1: 0 URLs\n\u2713 p2: 0 URLs\n")

    def test_urls_found(self):
        sys.argv = ['pep438', 'p1', 'p2']
        self.get_urls.side_effect = lambda p: ['1', '2'] if p == 'p1' else []
        with patch_io() as new:
            main()
            self.assertEqual(self.valid_package.call_count, 2)
            self.assertEqual(self.get_urls.call_count, 2)
            self.assertEqual(new.stderr.getvalue(), "")
            self.assertEqual(new.stdout.getvalue(),
                             "\u2717 p1: 2 URLs\n\u2713 p2: 0 URLs\n")

    def test_errors_only(self):
        sys.argv = ['pep438', '--errors-only', 'p1', 'p2']
        self.get_urls.side_effect = lambda p: ['1', '2'] if p == 'p1' else []
        with patch_io() as new:
            main()
            self.assertEqual(self.valid_package.call_count, 2)
            self.assertEqual(self.get_urls.call_count, 2)
            self.assertEqual(new.stderr.getvalue(), "")
            self.assertEqual(new.stdout.getvalue(), "\u2717 p1: 2 URLs\n")

    def test_invalid_package(self):
        self.valid_package.side_effect = lambda p: p != 'invalid'
        sys.argv = ['pep438', 'valid', 'invalid']
        with patch_io() as new:
            main()
            self.assertEqual(self.valid_package.call_count, 2)
            self.assertEqual(self.get_urls.call_count, 1)
            self.assertEqual(new.stderr.getvalue(),
                             "\u26a0 invalid: not found on PyPI\n")
            self.assertEqual(new.stdout.getvalue(),
                             "\u2713 valid: 0 URLs\n")

    @patch('pep438.main.get_pypi_user_packages')
    def test_pypi_user(self, user_packages):
        user_packages.side_effect = lambda u: ['p1']
        sys.argv = ['pep438', '-u', 'testuser']
        with patch_io() as new:
            main()
            user_packages.assert_called_once_with('testuser')
            self.valid_package.assert_called_once_with('p1')
            self.get_urls.called_once_with('p1')
            self.assertEqual(new.stdout.getvalue(), "\u2713 p1: 0 URLs\n")

    def test_version(self):
        for args in (['pep438', '-v'], ['pep438', '--version']):
            with patch_io() as new:
                sys.argv = args
                self.assertRaises(SystemExit, main)
                self.assertEqual(new.stdout.getvalue(),
                                 "pep438 version %s\n" % __version__)


if __name__ == '__main__':
    unittest.main()
