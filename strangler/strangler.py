import os

from strangler.violation_search import ViolationSearch


class Interface:
    def __init__(self, definition):
        # Describes the complete set of files within the module
        self.file_pattern = definition['file_pattern']
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
    ROOT_DIRECTORY = os.getcwd()

    def __init__(self, interface_definitions: dict, file_manager=None):
        self.violation_searcher = violation_searcher or ViolationSearch
        self.file_manager = file_manager or GrandfatherFileManager
        # TODO: validate interface definitions are well formed
        self.interface_definitions = interface_definitions

    def grandfather_violations(self):
        violations = self.interface_violations()
        self.file_manager.save(violations)

    def interface_violations(self):
        violations = []
        for definition in self.interface_definitions:
            violations.extend(self.violation_searcher.find_module_violations(definition))
        return violations

    def enforce_interfaces(self):
        if len(self.interface_violations()) > 0:
            raise InterfaceViolation()
