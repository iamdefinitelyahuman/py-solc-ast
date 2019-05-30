#!/usr/bin/python3

from .bases import NodeBase, ListNodeBase
from . import statements


def _get_nodes(node, type_, class_, parent):
    result = [i for i in node['nodes'] if i['nodeType'] == type_]
    for i in result:
        node['nodes'].remove(i)
    return [class_(i, parent) for i in result]


class SourceUnit(NodeBase, ListNodeBase):

    def __init__(self, node):
        self.depth = 0
        super().__init__(node, None)
        if node['nodeType'] != "SourceUnit":
            raise ValueError("Wrong node type - {}".format(node['nodeType']))
        self.path = node['absolutePath']
        self.contracts = _get_nodes(node, "ContractDefinition", ContractDefinition, self)
        ListNodeBase.__init__(self, self.contracts)


class ContractDefinition(NodeBase, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.functions = _get_nodes(node, "FunctionDefinition", FunctionDefinition, self)
        ListNodeBase.__init__(self, self.functions)


class FunctionDefinition(NodeBase, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        if node['body']:
            self.statements = statements.get_object(node.pop('body'), self)
        else:
            self.statements = []
        ListNodeBase.__init__(self, self.statements)
        if node['isConstructor']:
            self.name = "<constructor>"
        elif self.name is "":
            self.name = "<fallback>"
