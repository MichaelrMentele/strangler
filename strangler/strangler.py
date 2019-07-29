import os


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
        self.file_manager = file_manager or GrandfatherFileManager
        # TODO: validate interface definitions are well formed
        self.interface_definitions = interface_definitions

    def grandfather_violations(self):
        violations = self.interface_violations()
        self.file_manager.save(violations)

    def interface_violations(self):
        interface_to_violations = dict()
        for definition in self.interface_definitions:
            violations = self.find_interface_violations(definition)
            root_to_violations[definition['interface_name']] = violations

    def find_interface_violations(self, interface_definition) -> list:
        '''
        Traverses the list of module roots in the interface definitions and
        searches for import patterns that violate those definitions.
        '''
        # search for all matches given a particular definition
        # Where to search
        files_to_search = self.ROOT_DIRECTORY - definition['file_matcher'] - strangler_dir
        # TODO: all_imports_of_interface = search for imports of definition['root_module']
        # TODO: filtered_matches = exclude public matches unless also in private
        return filtered_matches

    def enforce_interfaces(self):
        if len(self.interface_violations()) > 0:
            raise InterfaceViolation()
