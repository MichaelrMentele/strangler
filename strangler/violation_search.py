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
        files = ViolationSearch._find_files_to_search(project_path, definition.module_file_path)
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
    def _find_files_to_search(project_path: str, root_file_path: str) -> list:
        '''
        Given a set of patterns, find all files from a search
        path. Then filter it down to files that don't match share
        a prefix
        '''
        all_project_files = [
            f for f in Path(project_path).glob('**/*')
            if f.is_file()
        ]

        # Filter out files that are within the root_file_path
        files_to_search = []
        for f in all_project_files:
            relative_file_path = f.absolute().relative_to(project_path).as_posix()
            # the root file path should not be a prefix (i.e. the file is within a dir)
            # AND the file path should not be within the root file path i.e the same file
            in_search_space = not root_file_path in relative_file_path and not relative_file_path in root_file_path
            valid_file = f.suffix == '.py'
            if in_search_space and valid_file:
                files_to_search.append(f)
        return files_to_search

    @staticmethod
    def _find_file_matches(f, regexes: List[str], project_root) -> list:
        '''
        Given a set of patterns and a file find all the lines that
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
