#!/usr/bin/python3

import json
from pathlib import Path

from .bases import NodeBase, ListNodeBase
from .definitions import ContractDefinition
from .utils import (
    get_node_objects,
    get_symbol_map
)


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


def set_dependencies(source_nodes):
    '''Sets contract node dependencies.

    Arguments:
        source_nodes: list of SourceUnit objects.

    Returns: SourceUnit objects where all ContractDefinition nodes contain
             'dependencies' and 'libraries' attributes.'''
    symbol_map = get_symbol_map(source_nodes)

    # add immediate dependencies
    for contract in [x for i in source_nodes for x in i]:
        contract.dependencies = set()

        # listed dependencies
        for key in contract._node['contractDependencies']:
            contract.dependencies.add(symbol_map[key])

        # using .. for libraries
        for node in [i for i in contract._node['nodes'] if i['nodeType'] == "UsingForDirective"]:
            contract._node['nodes'].remove(node)
            id_ = node['libraryName']['referencedDeclaration']
            contract.libraries[node['typeName']['name']] = symbol_map[id_]
            contract.dependencies.add(symbol_map[id_])

        # unlinked libraries
        for node in contract.children(filters={'node_type': "Identifier"}):
            if node.reference in symbol_map and symbol_map[node.reference].type == "library":
                contract.dependencies.add(symbol_map[node.reference])

    # add recursive dependencies
    for contract in [x for i in source_nodes for x in i]:
        for node in contract.dependencies.copy():
            contract.dependencies |= node.dependencies

    # convert dependency sets to lists
    for contract in [x for i in source_nodes for x in i]:
        contract.dependencies = sorted(contract.dependencies, key=lambda k: k.name)
    return source_nodes
