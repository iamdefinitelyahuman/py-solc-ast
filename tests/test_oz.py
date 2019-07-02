#!/usr/bin/python3

import solcast

# Check that loading the full open zeppelin contract set (as of July 1, 2019) does
# not raise any exceptions.


def test_from_json():
    solcast.from_standard_output_json('tests/open-zeppelin.json')
