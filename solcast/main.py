#!/usr/bin/python3

import json
from pathlib import Path


from .bases import NodeBase, ListNodeBase
from .definitions import ContractDefinition
from .utils import get_node_objects


def from_standard_output_json(path):
    '''Given the path to a json file containing standard compiler output,
    returns a list of SourceUnit objects.'''
    output_json = json.load(Path(path).open())
    return from_standard_output(output_json)


def from_standard_output(output_json):
    '''Given solc standard compiler output as a dict, returns a list of SourceUnit objects.'''
    symbols = {}
    sources = []
    for ast in [v['ast'] for v in output_json['sources'].values()]:
        sources.append(from_ast(ast))
        symbols.update((v[0], sources[-1][k]) for k, v in ast['exportedSymbols'].items())
    for contract in [x for i in sources for x in i]:
        contract.dependencies = []
        for key in contract._node['contractDependencies']:
            contract.dependencies.append(symbols[key])
        for node in [i for i in contract._node['nodes'] if i['nodeType'] == "UsingForDirective"]:
            contract._node['nodes'].remove(node)
            id_ = node['libraryName']['referencedDeclaration']
            contract.libraries[node['typeName']['name']] = symbols[id_]
    return sources


def from_ast(ast):
    return SourceUnit(ast['ast'] if 'ast' in ast else ast)


class SourceUnit(NodeBase, ListNodeBase):

    def __init__(self, node):
        self.depth = 0
        super().__init__(node, None)
        if node['nodeType'] != "SourceUnit":
            raise ValueError("Wrong node type - {}".format(node['nodeType']))
        self.name = node['absolutePath']
        self.contracts = get_node_objects(node, "ContractDefinition", ContractDefinition, self)
        ListNodeBase.__init__(self, self.contracts)
