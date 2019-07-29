from typing import List
from pathlib import Path
import re, os


def find_files(root_path: str, unix_file_pattern: str) -> list:
    '''
    Given a set of patterns, find all files from a search
    path.
    '''
    return list(Path(root_path).glob(unix_file_pattern))


def find_file_matches(f, regex_patterns: List[str], project_root) -> list:
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
    for pattern in regex_patterns:
        regex = re.compile(pattern)
        matches.extend(file_matches(f, regex))
    return matches
