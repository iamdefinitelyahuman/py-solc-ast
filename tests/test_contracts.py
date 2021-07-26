#!/usr/bin/python3

import json
from copy import deepcopy
from pathlib import Path

import pytest
import solcast

JSON_PATHS = list(Path("tests/compiled").glob("*.json"))


def test_dependencies():
    ast = solcast.from_standard_output_json("tests/compiled/aragon.json")
    node = next(i for i in ast[-1] if i.id == 16359)
    deps = set(i.name for i in node.dependencies)
    expected = {
        "Assert",
        "DelegateProxy",
        "ERCProxy",
        "IsContract",
        "ScriptHelpers",
        "Target",
        "ThrowProxy",
    }
    assert deps == expected


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


def test_dependencies_sol0_8_6():
    result = solcast.from_standard_output_json("tests/compiled/lp-token.json")
    lp_token_src = next(v for v in result if v.absolutePath == "./contracts/LpToken.sol")
    lp_token = lp_token_src["LpToken"]
    assert any(dep.name == "ERC20" for dep in lp_token.dependencies)
