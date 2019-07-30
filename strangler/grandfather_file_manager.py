import os


class GrandfatherFileManager:
    '''
    Responsible for storing strangler files and retrieving them given
    an interface definition.
    '''
    def __init__(self, root_dir_path, strangler_filepath='strangler_grandfathered_violations.txt'):
        self.strangler_filepath = os.path.join(root_dir_path, strangler_filepath)

    def save_grandfathered_violations(self, roottoviolations):
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
