from unittest import TestCase
import os

from strangler.violation_search import ViolationSearch
from strangler.strangler import Interface


class TestViolationSearch(TestCase):

    def test_find_module_violations(self):
        project_path = os.getcwd() + '/tests/test_data'

        # Scenario: Enforce one way imports
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'module_file_path': 'tests/test_data/one_way_imports/extensionBar',
                'module': 'extensionBar',
                # not defining public, implicitly means everything is public
            })
            # Since nothing is public we should throw errors if we export
            # and with this example we are exporting
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(
                violations,
                [('one_way_imports/extensionFoo.py', 2, 'from extensionBar import stuff\n'), ('one_way_imports/extensionFoo.py', 3, 'import extensionBar\n')]
            )

        # Scenarion: One way imports aren't enforced when public
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'module_file_path': 'tests/test_data/one_way_imports',
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
                'module_file_path': 'tests/test_data/one_way_imports/extensionBar',
                'module': 'extensionBar',
                'public': ['extensionBar'],
                'private': ['extensionBar'] # overrides public
            })
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(
                violations,
                [('one_way_imports/extensionFoo.py', 2, 'from extensionBar import stuff\n'), ('one_way_imports/extensionFoo.py', 3, 'import extensionBar\n')]
            )

        # Scenario: Cross module imports when public
        with self.subTest():
            interface = Interface({
                # files not to search and that define the internals of the module
                'module_file_path': 'tests/test_data/cross_imports/**/*.py',
                'module': 'cross_imports',
                'public': ['moduleB'],
                'private': [],
            })
            violations = ViolationSearch.find_module_violations(project_path, interface)
            self.assertEqual(len(violations), 0)

    def test_find_files_to_search(self):
        project_path = os.getcwd() + '/tests/test_data/one_way_imports'
        self.assertEqual(
            [f.name for f in ViolationSearch._find_files_to_search(project_path, 'extensionBar.py')],
            [
                'extensionFoo.py',
            ]

        )

    def test_find_file_matches(self):
        filename = 'extensionFoo.py'
        project_path = os.getcwd() + '/tests/test_data/one_way_imports/'
        files = ViolationSearch._find_files_to_search(project_path, 'one_way_imports/' + filename)
        assert len(files) == 1
        patterns = ['from.*{}.*$'.format('framework')]
        self.assertEqual(
            ViolationSearch._find_file_matches(files[0], patterns, project_path),
            [('extensionBar/extensionBar.py', 1, 'from framework.somewhere import FakeThingThatDoesntExist\n')]
        )
