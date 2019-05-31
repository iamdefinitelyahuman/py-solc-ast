#!/usr/bin/python3

import sys

from .bases import NodeBase, ListNodeBase


class Expression(NodeBase):

    _count = {}

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self._count.setdefault(self.node_type, 0)
        self._count[self.node_type] += 1
        for key, value in [(k, v) for k, v in node.items() if type(v) is list and v]:
            if type(value[0]) is dict and 'nodeType' in value[0]:
                setattr(self, key, get_objects(value), self)
        for key, value in [(k, v) for k, v in node.items() if type(v) is dict]:
            if 'nodeType' in value:
                setattr(self, key, get_object(value, self))


class NewExpression(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.type = get_object(node.pop('typeName'), self)


class IndexAccess(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.base = get_object(node.pop('baseExpression'), self)
        self.index = get_object(node.pop('indexExpression'), self)
        self.name = "{}[{}]".format(self.base._display(), self.index._display())


class MemberAccess(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.expression = get_object(node.pop('expression'), self)
        self.name = self.expression._display()+"."+node['memberName']


class FunctionCall(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.expression = get_object(node.pop('expression'), self)
        self.arguments = get_objects(node.pop('arguments'), self)
        self.name = self.expression.name

    def _display(self):
        return (
            self.expression._display() + "(" +
            (", ".join(i._display() for i in self.arguments)) + ")"
        )


class Literal(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.type = node['kind']

    def _display(self):
        return self.value


class TupleExpression(NodeBase, ListNodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.components = get_objects(node.pop('components'), self)
        ListNodeBase.__init__(self, self.components)
        self.name = node['typeDescriptions']['typeString']

    def _display(self):
        return "{}=({})".format(self.name, ", ".join(i._display() for i in self.components))


class Identifier(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.reference = node['referencedDeclaration']


class ElementaryTypeName(NodeBase):
    pass


class ElementaryTypeNameExpression(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.name = node['typeName']


class UserDefinedTypeName(NodeBase):
    pass


class ArrayTypeName(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.type = get_object(node.pop('baseType'), self)
        self.name = node['typeDescriptions']['typeString']


class Mapping(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.key = get_object(node.pop('keyType'), self)
        self.value = get_object(node.pop('valueType'), self)


class VariableDeclaration(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.type = get_object(node.pop('typeName'), self)


class UnaryOperation(NodeBase):

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.expression = get_object(node.pop('subExpression'), self)
        if node['prefix']:
            self.name = node['operator']+(self.expression.name or self.expression.value)
        else:
            self.name = self.expression.name+node['operator']


class _TwoSidedExpression(NodeBase, ListNodeBase):

    def __init__(self, node, parent, key):
        super().__init__(node, parent)
        self.left = get_object(node.pop('left'+key), self)
        self.right = get_object(node.pop('right'+key), self)
        self.operator = node.pop('operator')
        self.type = node['typeDescriptions']['typeString']
        ListNodeBase.__init__(self, [self.left, self.right])

    def _display(self):
        return "{} {} {}".format(self.left._display(), self.operator, self.right._display())


class BinaryOperation(_TwoSidedExpression):

    def __init__(self, node, parent):
        super().__init__(node, parent, 'Expression')


class Assignment(_TwoSidedExpression):

    def __init__(self, node, parent):
        super().__init__(node, parent, 'HandSide')


class Conditional(NodeBase):

    '''Ternery operator'''

    def __init__(self, node, parent):
        super().__init__(node, parent)
        self.condition = get_object(node.pop('condition'), self)
        self.true = get_object(node.pop('trueExpression'), self)
        self.false = get_object(node.pop('falseExpression'), self)

    def _display(self):
        return (
            self.condition._display() + " ? " +
            self.true._display() + " | " +
            self.false._display()
        )


def get_object(node, parent):
    return get_class(node)(node, parent)


def get_objects(node_list, parent):
    return [get_object(i, parent) for i in node_list if i]


def get_class(node):
    try:
        return getattr(sys.modules[__name__], node['nodeType'])
    except AttributeError:
        return Expression
