#!/usr/bin/python3

import json
from pathlib import Path


from .bases import NodeBase, ListNodeBase
from .definitions import ContractDefinition
from .utils import get_node_objects


def from_ast(ast):
    return SourceUnit(ast['ast'] if 'ast' in ast else ast)


def from_json(path):
    ast = json.load(Path(path).open())
    return from_ast(ast)


class SourceUnit(NodeBase, ListNodeBase):

    def __init__(self, node):
        self.depth = 0
        super().__init__(node, None)
        if node['nodeType'] != "SourceUnit":
            raise ValueError("Wrong node type - {}".format(node['nodeType']))
        self.path = node['absolutePath']
        self.contracts = get_node_objects(node, "ContractDefinition", ContractDefinition, self)
        ListNodeBase.__init__(self, self.contracts)
