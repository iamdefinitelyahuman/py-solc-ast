#!/usr/bin/python3

from .bases import NodeBase, ListNodeBase
from . import statements
from .utils import get_node_objects


class Definition(NodeBase):

    node_class = "Definition"

    def __init__(self, node, parent):
        super().__init__(node, parent)


class ContractDefinition(Definition, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.functions = get_node_objects(node, "FunctionDefinition", FunctionDefinition, self)
        ListNodeBase.__init__(self, self.functions)


class FunctionDefinition(Definition, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        if node['body']:
            self.statements = statements.get_object(node.pop('body'), self)
        else:
            self.statements = []
        ListNodeBase.__init__(self, self.statements)
        if self.name:
            return
        if 'kind' in node and node['kind'] != "function":
            self.name = '<{}>'.format(node['kind'])
        elif 'isConstructor' in node and node['isConstructor']:
            self.name = "<constructor>"
        else:
            self.name = "<fallback>"
