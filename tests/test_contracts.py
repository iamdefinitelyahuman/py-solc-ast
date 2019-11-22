#!/usr/bin/python3

import json
from copy import deepcopy
from pathlib import Path

import pytest
import solcast

JSON_PATHS = list(Path("tests/compiled").glob("*.json"))


@pytest.mark.parametrize("path", JSON_PATHS)
def test_solcast(path):
    solcast.from_standard_output_json(path)


@pytest.mark.parametrize("path", JSON_PATHS)
def test_mutation(path):
    with open(path) as fp:
        output_json = json.load(fp)
    original = deepcopy(output_json)
    solcast.from_standard_output(output_json)
    assert original == output_json
