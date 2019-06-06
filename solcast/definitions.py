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
        self.type = node['contractKind']
        self.libraries = dict((
            i['typeName']['name'],
            i['libraryName']['name']
        ) for i in node['nodes'] if i['nodeType'] == "UsingForDirective")
        self.modifiers = get_node_objects(node, "ModifierDefinition", ModifierDefinition, self)
        self.functions = get_node_objects(node, "FunctionDefinition", FunctionDefinition, self)
        ListNodeBase.__init__(self, self.functions)


class ModifierDefinition(Definition, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.statements = statements.get_object(node.pop('body'), self)
        ListNodeBase.__init__(self, self.statements)
        self.full_name = "{0._parent.name}.{0.name}".format(self)


class FunctionDefinition(Definition, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        if node['body']:
            self.statements = statements.get_object(node.pop('body'), self)
        else:
            self.statements = []
        ListNodeBase.__init__(self, self.statements)
        self.modifiers = [i['modifierName']['name'] for i in node.pop('modifiers')]
        if not self.name:
            if 'kind' in node and node['kind'] != "function":
                self.name = '<{}>'.format(node['kind'])
            elif 'isConstructor' in node and node['isConstructor']:
                self.name = "<constructor>"
            else:
                self.name = "<fallback>"
        self.full_name = "{0._parent.name}.{0.name}".format(self)
