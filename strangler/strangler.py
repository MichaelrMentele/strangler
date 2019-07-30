import os

from strangler.grandfather_file_manager import GrandfatherFileManager
from strangler.violation_search import ViolationSearch


class Interface:
    def __init__(self, definition):
        # Describes the complete set of files within the module
        self.module_file_path = definition['module_file_path']
        # Module name
        self.module = definition['module']
        self.public = definition.get('public', [])
        self.private = definition.get('private', [])


class StranglerInterfaceViolation(Exception):
    pass


class Strangler:
    # The root directory is analagous to defining the entire search space
    # for an interface definition to be checked against, that is what is
    # outside of the module
    ROOT_DIRECTORY = os.getcwd() + '/strangler'

    def __init__(self, interface_definitions: dict, file_manager=None, violation_searcher=None):
        self.violation_searcher = violation_searcher or ViolationSearch
        self.file_manager = file_manager or GrandfatherFileManager(self.ROOT_DIRECTORY)
        # TODO: validate interface definitions are well formed
        self.interface_definitions = interface_definitions

    def grandfather_violations(self):
        violations = self.report_violations()
        self.file_manager.save(violations)

    def report_violations(self):
        whitelisted_violations = self.file_manager.read()
        violations = []
        for definition in self.interface_definitions:
            candidates = self.violation_searcher.find_module_violations(self.ROOT_DIRECTORY, definition)
            actual_violations = [
                candidate for candidate in candidates
                if candidate not in whitelisted_violations
            ]
            violations.extend(actual_violations)
        return violations

    def enforce_violations(self):
        if len(self.report_violations()) > 0:
            raise StranglerInterfaceViolation
