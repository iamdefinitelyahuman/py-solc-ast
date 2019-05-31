#!/usr/bin/python3

import json
from pathlib import Path

from .bases import NodeBase, ListNodeBase
from .definitions import ContractDefinition
from .utils import (
    set_dependencies,
    get_node_objects,
)


def from_standard_output_json(path):
    '''Generates SourceUnit objects from a standard output json file.

    Arguments:
        path: path to the json file'''
    output_json = json.load(Path(path).open())
    return from_standard_output(output_json)


def from_standard_output(output_json):
    '''Generates SourceUnit objects from a standard output json as a dict.

    Arguments:
        output_json: dict of standard compiler output'''
    source_nodes = [SourceUnit(v['ast']) for v in output_json['sources'].values()]
    source_nodes = set_dependencies(source_nodes)
    return source_nodes


class SourceUnit(NodeBase, ListNodeBase):

    def __init__(self, node):
        if 'ast' in node:
            node = node['ast']
        self.depth = 0
        super().__init__(node, None)
        if node['nodeType'] != "SourceUnit":
            raise ValueError("Wrong node type - {}".format(node['nodeType']))
        self.name = node['absolutePath']
        self.path = node['absolutePath']
        self.contracts = get_node_objects(node, "ContractDefinition", ContractDefinition, self)
        ListNodeBase.__init__(self, self.contracts)
