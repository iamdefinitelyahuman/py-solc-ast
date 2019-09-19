#!/usr/bin/python3

import solcast

# Check that loading the open zeppelin contract set (as of July 1, 2019) does not raise
# https://github.com/OpenZeppelin/openzeppelin-contracts


def test_open_zeppelin():
    solcast.from_standard_output_json("tests/open-zeppelin.json")


# Check that loading AragonOS contract set (as of July 28, 2019) does not raise
# https://github.com/aragon/aragonOS


def test_aragon():
    solcast.from_standard_output_json("tests/aragon.json")
