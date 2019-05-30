#!/usr/bin/python3

from .bases import ListNodeBase
from . import statements


def _get_nodes(node, type_, class_, parent):
    result = [i for i in node['nodes'] if i['nodeType'] == type_]
    for i in result:
        node['nodes'].remove(i)
    return [class_(i, parent) for i in result]


class SourceUnit(ListNodeBase):

    def __init__(self, node):
        self.depth = 0
        if node['nodeType'] != "SourceUnit":
            raise ValueError("Wrong node type - {}".format(node['nodeType']))
        self.path = node['absolutePath']
        self.contracts = _get_nodes(node, "ContractDefinition", ContractDefinition, self)
        super().__init__(node, None, [self.contracts])


class ContractDefinition(ListNodeBase):

    def __init__(self, node, parent):
        self.depth = parent.depth + 1
        self.functions = _get_nodes(node, "FunctionDefinition", FunctionDefinition, self)
        super().__init__(node, parent, [self.functions])


class FunctionDefinition(ListNodeBase):

    def __init__(self, node, parent):
        self.depth = parent.depth + 1
        if node['body']:
            self.statements = statements.get_object(node.pop('body'), self)
        else:
            self.statements = []
        super().__init__(node, parent, [self.statements])
        if node['isConstructor']:
            self.name = "<constructor>"
        elif self.name is "":
            self.name = "<fallback>"
