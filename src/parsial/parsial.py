"""
Python library that transforms any string parser into a parser
that skips lines containing syntax errors.
"""
from __future__ import annotations
from typing import Any, List, Callable
import doctest

def parsial(parse: Callable[[str], Any]) -> Callable[[str], List[int]]:
    """
    Accept a parsing function that takes string inputs and return a function
    that returns some subset of the lines in the input string that, when
    removed, allow the the parsing function to succeed.
    """
    # Define the new parsing function.
    def parse_(source: str) -> List[int]:
        lines = source.split('\n')
        for end in range(len(lines), -1, -1):
            try:
                parse('\n'.join(lines[:end]))
                lines_ = lines[:end]
                break
            except Exception as _:
                pass

        skips = []
        if end < len(lines):
            skips.append(end)
            lines_ = lines[:end] + ['']
            for i in range(end + 1, len(lines)):
                try:
                    lines__ = lines_ + [lines[i]]
                    parse('\n'.join(lines__))
                    lines_ = lines__
                except Exception as _:
                    lines_ += ['']
                    skips.append(i)

        return skips

    return parse_

if __name__ == '__main__':
    doctest.testmod()
