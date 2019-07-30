import os
from ast import literal_eval # TODO: replace with parsing


class GrandfatherFileManager:
    '''
    Responsible for storing strangler files and retrieving them given
    an interface definition.
    '''
    def __init__(self, root_dir_path, strangler_filepath='strangler_grandfathered_violations.txt'):
        self.strangler_filepath = os.path.join(root_dir_path, strangler_filepath)
        self.filename = 'strangler_grandfathered_violations.txt'

    def save(self, violations):
        with open(self.filename, 'w+') as grandfather_file:
            for violation in violations:
                grandfather_file.write(str(violation)+'\n')

    def read(self):
        try:
            with open(self.filename, 'r') as grandfather_file:
                lines = grandfather_file.readlines()
                grandfathered_violations = [literal_eval(line) for line in lines]
            return grandfathered_violations
        except FileNotFoundError:
            return []

    def delete(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass
