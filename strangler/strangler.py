import os


class GrandfatherFileManager:
    '''
    Responsible for storing strangler files and retrieving them given
    a module path.
    '''
    def __init__(self, root_dir_path, strangler_dir_name='strangler'):
        self.strangler_dir = os.path.join(root_dir, strangler_dir_name)

    def _convert_to_filename(self, module_path):
        return  self.strangler_dir + '/' + filename + module_path.replace('.', '-')

    def save_all_grandfather_files(self, roottoviolations):
        for root_module, violations in nametoviolations.items():
            save_grandfather_file(root_module, violations)

    def save_grandfather_file(self, module_path, contents):
        filepath = self._get_path(module_path)
        with open(filename, 'w+') as grandfather_file:
            for line in contents:
                grandfather_file.write(line)

    def read(self, module_path) -> list:
        filepath = self._get_path(module_path)
        return open(filepath, 'r').read()

    def has_shrunk(self, module_path):
        pass

    def has_grown(self, module_path):
        pass


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
