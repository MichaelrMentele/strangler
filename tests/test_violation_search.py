from unittest import TestCase
import os

from strangler.violation_search import ViolationSearch


class TestViolationSearch(TestCase):
    def test_find_files(self):
        self.assertEqual(
            [f.name for f in ViolationSearch._find_files('', '**/test_violation_search.py')],
            ['test_violation_search.py']
        )

    def test_find_file_matches(self):
        filename = 'violation_search.py'
        f = ViolationSearch._find_files('.', '**/' + filename)[0]
        patterns = ['.*import .*List.*$', '.*import.*Path.*$']
        self.assertEqual(
            ViolationSearch._find_file_matches(f, patterns, os.getcwd()),
            [
                (filename, 1, 'from typing import List\n'),
                (filename, 2, 'from pathlib import Path\n'),
            ]
        )
