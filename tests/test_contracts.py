#!/usr/bin/python3

from pathlib import Path

import pytest
import solcast

JSON_PATHS = list(Path("tests/compiled").glob("*.json"))


@pytest.mark.parametrize("path", JSON_PATHS)
def test_solcast(path):
    solcast.from_standard_output_json(path)
