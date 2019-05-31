#!/usr/bin/python3


class NodeBase:

    def __init__(self, node, parent):
        self._node = node
        self.node_type = node['nodeType']
        self.name = node['name'] if 'name' in node else None
        self.value = node['value'] if 'value' in node else None
        src = [int(i) for i in node['src'].split(':')]
        self.offset = [src[0], src[0]+src[1]]
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

    def __eq__(self, other):
        if type(other) is str:
            return self.node_type == other
        return super().__eq__(other)

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

    def keys(self):
        return [i for i in dir(self) if not i.startswith('_')]

    def children(self, depth=None, include_self=False, include_parents=True, **filters):
        '''Get childen nodes of this node.

        Arguments:
          depth: Number of levels of children to traverse. 0 returns only this node.
          include_self: Includes this node in the results.
          include_parents: Includes nodes that match in the results, when they also have
                        child nodes that match.

        Keyword Arguments:
          **filters: Attribute name:value pairs that nodes must match to return. If left
                     blank, all nodes are returned.

        Returns:
            List of node objects.'''
        if depth is not None:
            depth -= 1
            if depth < 0:
                return [self] if (include_self and _check_filters(self, filters)) else []
        result = []
        for obj in [getattr(self, i) for i in self.keys() if i != "parent"]:
            if type(obj) is list and obj and hasattr(obj[0], 'node_type'):
                for node in obj:
                    result.extend(node.children(depth, True, include_parents, **filters))
            elif hasattr(obj, 'node_type'):
                result.extend(obj.children(depth, True, include_parents, **filters))
        if include_self and _check_filters(self, filters) and (include_parents or not result):
            result.insert(0, self)
        return result


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


def _check_filters(node, filters):
    for key, value in filters.items():
        if not hasattr(node, key) or getattr(node, key) != value:
            return False
    return True
