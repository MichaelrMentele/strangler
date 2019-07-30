import os


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
                grandfather_file.write(str(violation))
