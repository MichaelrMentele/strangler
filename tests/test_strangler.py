from unittest import TestCase
import os

from strangler.grandfather_file_manager import GrandfatherFileManager
from strangler.strangler import Strangler, Interface, StranglerInterfaceViolation


class TestStrangler(TestCase):
    def setUp(self):
        interface = Interface({
            # files not to search and that define the internals of the module
            'module_file_path': 'tests/test_data/one_way_imports/extensionBar',
            'module': 'extensionBar',
            # not defining public, implicitly means everything is public
        })
        self.strangler = Strangler([interface])
        self.strangler.ROOT_DIRECTORY = os.getcwd() + '/tests/test_data/one_way_imports'
        self.strangler.file_manager.delete()

    def test_report_violations(self):
        self.assertEqual(
            self.strangler.report_violations(),
            [('extensionFoo.py', 2, 'from extensionBar import stuff\n'), ('extensionFoo.py', 3, 'import extensionBar\n')]
        )

    def test_enforce_violations(self):
        with self.assertRaises(StranglerInterfaceViolation):
            self.strangler.enforce_violations()

    def test_grandfather_violations(self):
        self.strangler.grandfather_violations()

    def test_enforce_violations_when_grandfathered(self):
        self.strangler.grandfather_violations()
        self.strangler.enforce_violations() # doesn't raise
