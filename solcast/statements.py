#!/usr/bin/python3

import sys

from .bases import NodeBase, ListNodeBase
from . import expressions


class Statement(NodeBase):

    node_class = "Statement"

    def __init__(self, node, parent):
        super().__init__(node, parent)


class IfStatement(Statement, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.condition = expressions.get_object(node.pop('condition'), self)
        for key in ['trueBody', 'falseBody']:
            body = get_object(node.pop(key), self) if node[key] else []
            setattr(self, key[:-4], body if type(body) is list else [body])
        ListNodeBase.__init__(self, self.true + self.false)


class WhileStatement(Statement):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.condition = expressions.get_object(node.pop('condition'), self)
        self.body = get_object(node.pop('body'), self)


class ForStatement(Statement, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.init = get_object(node.pop('initializationExpression'), self)
        self.condition = expressions.get_object(node.pop('condition'), self)
        self.loop = get_object(node.pop('loopExpression'), self)
        self.body = get_object(node.pop('body'), self)
        ListNodeBase.__init__(self, self.body)


class VariableDeclarationStatement(Statement):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.declarations = expressions.get_objects(node.pop('declarations'), self)
        if node['initialValue']:
            self.initial_value = expressions.get_object(node.pop('initialValue'), self)
        else:
            self.initival_value = None


class ExpressionStatement(Statement):

    def __init__(self, node, parent):
        super().__init__(node.pop('expression'), parent)


class Return(Statement):

    def __init__(self, node, parent):
        super().__init__(node.pop('expression') or node, parent)


class EmitStatement(Statement):

    def __init__(self, node, parent):
        name = node['eventCall']['expression']['name']
        super().__init__(node.pop('eventCall'), parent)
        src = [int(i) for i in node['src'].split(':')]
        self.offset = (src[0], src[0]+src[1])
        self.name = name


def get_object(node, parent):
    if node['nodeType'] in ("ExpressionStatement", "Return"):
        class_ = type(
            node['nodeType'],
            (
                getattr(sys.modules[__name__], node['nodeType']),
                expressions.get_class(node['expression'] or node)
            ),
            {}
        )
        return class_(node, parent)
    if node['nodeType'] == "Block":
        return get_objects(node.pop('statements'), parent)
    try:
        class_ = getattr(sys.modules[__name__], node['nodeType'])
    except AttributeError:
        class_ = Statement
    return class_(node, parent)


def get_objects(node_list, parent):
    return [get_object(i, parent) for i in node_list]
