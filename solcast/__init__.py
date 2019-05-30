#!/usr/bin/python3

import json
from pathlib import Path

from .definitions import SourceUnit


def from_ast(ast):
    return SourceUnit(ast['ast'] if 'ast' in ast else ast)


def from_json(path):
    ast = json.load(Path(path).open())
    return from_ast(ast)
