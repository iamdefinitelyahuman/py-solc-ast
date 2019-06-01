#!/usr/bin/python3

from .utils import is_inside_offset


class NodeBase:

    def __init__(self, node, parent):
        self._node = node
        self.node_type = node['nodeType']
        self.name = node['name'] if 'name' in node else None
        self.value = node['value'] if 'value' in node else None
        src = [int(i) for i in node['src'].split(':')]
        self.offset = (src[0], src[0]+src[1])
        self.contract_id = src[2]
        self.parent = parent
        self.depth = parent.depth + 1 if parent is not None else 0

    def __hash__(self):
        return hash("{0.node_type}{0.depth}{0.offset}{0.name}".format(self))

    def __repr__(self):
        name = type(self).__name__
        repr_str = "<" + name
        if self.node_type != name:
            repr_str += "." + self.node_type
        if hasattr(self, '_iter_list'):
            repr_str += " iterable"
        if hasattr(self, 'type'):
            if type(self.type)is str:
                repr_str += " " + self.type
            else:
                repr_str += " " + self.type._display()
        if self._display():
            repr_str += " '" + self._display() + "'"
        else:
            repr_str += " object"
        return repr_str+">"

    def _display(self):
        if self.name and self.value:
            return "'{}' = {}".format(self.name, self.value)
        return self.name or self.value or ""

    def _unimplemented(self):
        '''Returns a list of keys that lead to child nodes that have not yet
        been implemented within py-solc-ast.'''
        return [
            k for k, v in self._node.items() if type(v) is dict and 'nodeType' in v or
            type(v) is list and v and type(v[0]) is dict and 'nodeType' in v[0]
        ]

    def _children(self):
        node_list = []
        for obj in [getattr(self, i) for i in self.keys() if i != "parent"]:
            if type(obj) is list and obj and hasattr(obj[0], 'node_type'):
                node_list.extend([i for i in obj if i.depth == self.depth + 1])
            elif hasattr(obj, 'node_type') and obj.depth == self.depth + 1:
                node_list.append(obj)
        return node_list

    def keys(self):
        return [i for i in dir(self) if not i.startswith('_')]

    def children(
        self,
        depth=None,
        include_self=False,
        include_parents=True,
        filters={},
        exclude={}
    ):
        '''Get childen nodes of this node.

        Arguments:
          depth: Number of levels of children to traverse. 0 returns only this node.
          include_self: Includes this node in the results.
          include_parents: Includes nodes that match in the results, when they also have
                        child nodes that match.
          filters: Dictionary of {attribute: value} that children must match. Can also
                   be given as a list of dicts, children that match one of the dicts
                   will be returned.
          exclude: Dictionary of {attribute:value} that children cannot match.

        Returns:
            List of node objects.'''
        if depth is not None:
            depth -= 1
            if depth < 0:
                return [self] if (include_self and _check_filters(self, filters, exclude)) else []
        node_list = []
        for node in self._children():
            node_list.extend(node.children(depth, True, include_parents, filters, exclude))
        if (
            include_self and
            (include_parents or not node_list) and
            _check_filters(self, filters, exclude)
        ):
            node_list.insert(0, self)
        return node_list

    def child_by_offset(self, offset, exact=False):
        '''Get an immediate child node based on a source offset.

        Arguments:
            offset: A source offset as (start, stop)
            exact: If False, returns a child where the given offset is contained
                   inside the child's offset. If True, only returns an exact match.

        Returns:
            Node object.'''
        try:
            if exact:
                return next(i for i in self._children() if tuple(offset) == i.offset)
            return next(i for i in self._children() if is_inside_offset(offset, i.offset))
        except StopIteration:
            raise KeyError(
                "No node with {}offset match of {}".format("exact " if exact else "", offset)
            )

    def root(self, depth=1):
        '''Returns the parent node object at the given depth.'''
        if depth >= self.depth:
            raise ValueError("Given depth exceeds object depth")
        parent = self.parent
        while parent.depth > depth:
            parent = parent.parent
        return parent

    def is_child_of(self, node):
        '''Checks if the given node object is a child of this object.'''
        if node.depth >= self.depth:
            return False
        return self.root(node.depth) == node


class ListNodeBase:

    def __init__(self, iter_list):
        self._iter_list = iter_list

    def __getitem__(self, key):
        if type(key) is str:
            try:
                return next(i for i in self._iter_list if i.name == key)
            except StopIteration:
                raise KeyError(key)
        return self._iter_list[key]

    def __iter__(self):
        return iter(self._iter_list)

    def __len__(self):
        return len(self._iter_list)

    def __contains__(self, obj):
        return obj in self._iter_list


def _check_filters(node, filters, exclude):
    if type(filters) is dict:
        return _check_filter(node, filters, exclude)
    for f in filters:
        if _check_filter(node, f, exclude):
            return True
    return False


def _check_filter(node, filters, exclude):
    for key, value in filters.items():
        if not hasattr(node, key) or getattr(node, key) != value:
            return False
    for key, value in exclude.items():
        if hasattr(node, key) and getattr(node, key) == value:
            return False
    return True
