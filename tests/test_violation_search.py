from unittest import TestCase
import os

from strangler.violation_search import ViolationSearch
from strangler.strangler import Interface


class TestViolationSearch(TestCase):

    def test_find_module_violations(self):
        project_path = os.getcwd()

        # Scenario: Enforce one way imports
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'file_pattern': 'tests/test_data/one_way_imports/**/*.py',
                'module': 'extensionBar',
                # not defining public, implicitly means everything is public
            })
            # Since nothing is public we should throw errors if we export
            # and with this example we are exporting
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(len(violations), 1)
            self.assertEqual(
                violations,
                [('tests/test_data/one_way_imports/extensionFoo.py', 2, 'from extensionBar import stuff\n')]
            )

        # Scenarion: One way imports aren't enforced when public
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'file_pattern': 'tests/test_data/one_way_imports/**/*.py',
                'module': 'extensionBar',
                'public': ['extensionBar']
            })
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(len(violations), 0)
            self.assertEqual(violations, [])

        # Scenario One: way imports with public overriden by private
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'file_pattern': 'tests/test_data/one_way_imports/**/*.py',
                'module': 'extensionBar',
                'public': ['extensionBar'],
                'private': ['extensionBar'] # overrides public
            })
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(len(violations), 1)
            self.assertEqual(
                violations,
                [('tests/test_data/one_way_imports/extensionFoo.py', 2, 'from extensionBar import stuff\n')]
            )

        # Scenario: Cross module imports when public
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'file_pattern': 'tests/test_data/cross_imports/**/*.py',
                'module': 'cross_imports',
                'public': ['moduleB'],
                'private': [],
            })
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(len(violations), 0)

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
                ('strangler/' + filename, 1, 'from typing import List\n'),
                ('strangler/' + filename, 2, 'from pathlib import Path\n'),
            ]
        )
