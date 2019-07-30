from typing import List
from pathlib import Path
import re, os


class ViolationSearch:
    @staticmethod
    def find_module_violations(project_path, definition):
        '''
        Accepts a module name that we will search for import from, then
        checks those module import patterns against all files that match
        the file pattern.

        This is then filtered down, where anything that matches what is
        public for that module and is NOT explicitly private, is excluded.
        Why is it excluded? Because it is a valid export.
        '''
        # Find all exports for this module
        regexes = ViolationSearch._construct_regex_from_module(definition.module)
        files = ViolationSearch._find_files(project_path, definition.file_pattern)
        violations = []
        for f in files:
            matches = ViolationSearch._find_file_matches(f, regexes, project_path)
            if matches: violations.extend(matches)

        # Filter down to actual violations:
        # 1. is public
        # 2. is not explicitly private
        return [
            violation for violation in violations
            # It's a violation if the import is not public AKA private OR it is private
            if not (any([re.findall(pattern, violation[-1]) for pattern in definition.public])) or
                any([re.findall(pattern, violation[-1]) for pattern in definition.private])
        ]

    @staticmethod
    def _construct_regex_from_module(module):
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
        return [
            f for f in Path(project_path).glob(unix_file_pattern)
            if f.is_file()
        ]

    @staticmethod
    def _find_file_matches(f, regexes: List[str], project_root) -> list:
        '''
        Given a set of patterns and files find all the lines that
        match.
        '''

        def file_matches(f, regex) -> list:
            matches = []
            for lineno, line in enumerate(open(f)):
                if re.match(regex, line):
                    project_relative_path = f.absolute().relative_to(project_root).as_posix()
                    matches.append((project_relative_path, lineno + 1, line))
            return matches

        matches = []
        for regex in regexes:
            matches.extend(file_matches(f, regex))
        return matches
