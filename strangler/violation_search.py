from typing import List
from pathlib import Path
import re, os


class ViolationSearch:
    @staticmethod
    def find_module_violations(filepattern, module):
        regexes = ViolationSearch._construct_regex_from_modules(module)
        files = ViolationSearch._find_files(project_path, filepattern)
        violations = []
        for f in files:
            violations.append(self._find_file_matches(f, regexes, project_root))
        return violations

    @staticmethod
    def _construct_regex_from_modules(module):
        patterns = []
        patterns.append(re.compile('^from .*{}.*$'.format(module)))
        patterns.append(re.compile('^import .*{}.*$'.format(module)))
        return patterns

    @staticmethod
    def _find_files(project_path: str, unix_file_pattern: str) -> list:
        '''
        Given a set of patterns, find all files from a search
        path.
        '''
        return list(Path(project_path).glob(unix_file_pattern))

    @staticmethod
    def _find_file_matches(f, regexes: List[str], project_root) -> list:
        '''
        Given a set of patterns and files find all the lines that
        match.
        '''
        def relativize(path, relative_root):
            prefix = os.path.commonprefix([path, relative_root])
            # trim out the prefix from abs_path
            # add 1 to account for the leading forward slash
            return path[len(prefix) + 1:]

        def file_matches(f, regex) -> list:
            matches = []
            for lineno, line in enumerate(open(f)):
                if re.match(regex, line):
                    matches.append((relativize(os.path.abspath(f.name), project_root), lineno + 1, line))
            return matches

        matches = []
        for regex in regexes:
            matches.extend(file_matches(f, regex))
        return matches
