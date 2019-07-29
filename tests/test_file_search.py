from unittest import TestCase
import os

from strangler.file_search import find_files, find_file_matches


class TestFindFiles(TestCase):
    def test_find_files(self):
        self.assertEqual(
            [f.name for f in find_files('.', '**/test_file_search.py')],
            ['test_file_search.py']
        )


class TestFindFileMatches(TestCase):
    def test_find_file_matches(self):
        filename = 'file_search.py'
        f = find_files('.', '**/' + filename)[0]
        patterns = ['.*import .*List.*$', '.*import.*Path.*$']
        self.assertEqual(
            find_file_matches(f, patterns, os.getcwd()),
            [
                (filename, 1, 'from typing import List\n'),
                (filename, 2, 'from pathlib import Path\n'),
            ]
        )
