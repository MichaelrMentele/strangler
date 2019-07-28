from typing import List
from pathlib import Path
import re


def find_files(root_path: str, unix_file_pattern: str) -> list:
    '''
    Given a set of patterns, find all files from a search
    path.
    '''
    return list(Path(root_path).glob(unix_file_pattern))


def find_file_matches(f, regex_patterns: List[str]) -> list:
    '''
    Given a set of patterns and files find all the lines that
    match.
    '''
    def file_matches(f, regex) -> list:
        matches = []
        for lineno, line in enumerate(open(f)):
            if re.match(regex, line):
                matches.append((f.name, lineno + 1, line))
        return matches

    matches = []
    for pattern in regex_patterns:
        regex = re.compile(pattern)
        matches.extend(file_matches(f, regex))
    return matches
