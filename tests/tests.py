
class TestGrandfatherFileManager(TestCase):
    def test_generate_name(self):
        # names_grandfather_files_appropriately
        pass

    def test_save(self):
        # saves the grandfather file to the correct path
        pass

    def test_fetch(self):
        # returns the matches as a list
        pass


class TestStranglerInvalidConfig(TestCase):
    def setUp(self):
        self.config = {
            'search_space': '~/Personal/strangler',
            'interface_definitions': []
        }

        self.definition_template = {
            'interface_name': None
            'module_root': "cross_imports"
            'file_root': 'test_data/cross_imports'
            'rules': [
            ]
        }

    def test_validate_definitions(self):
        # Raises when no rules defined
        # Raises when no public defined, only private for a rule
        # Raises when invalid pattern
        # Otherwise valid and no raise
        pass


class TestStranglerCrossImportsScenario(TestCase):
    def setUp(self):
        self.config = {
            'search_space': '~/Personal/strangler',
            'interface_definitions': {}
        }

        self.definition_template = {
            'module_root': "cross_imports"
            'file_matcher': 'test_data/cross_imports*'
            'rules': [
            ]
        }

    def test_cross_imports_allowed(self):
        self.definition_template['rules'].append({
            'searchable_scope':
            'public': '*',
            'private': []
        })
        self.config['interface_definitions']['Allow All Exports'] = self.definition_template

    def test_cross_imports_disallowed_from_A_into_B(self):
        pass

    def test_all_cross_imports_allowed(self):
        pass


class TestStranglerOneWayImportsScenario(TestCase):
