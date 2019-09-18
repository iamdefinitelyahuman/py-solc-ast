#!/usr/bin/python3

import functools


class NodeBase:
    def __init__(self, ast, parent):
        self.depth = parent.depth + 1 if parent is not None else 0
        self._parent = parent
        self._children = set()
        src = ast["src"]
        self.offset = (src[0], src[0] + src[1])
        for key, value in ast.items():
            if isinstance(value, dict) and value.get("nodeType") == "Block":
                value = value["statements"]
            elif key == "body" and not value:
                value = []
            if isinstance(value, dict):
                item = node_class_factory(value, self)
                if isinstance(item, NodeBase):
                    self._children.add(item)
                setattr(self, key, item)
            elif isinstance(value, list):
                items = [node_class_factory(i, self) for i in value]
                setattr(self, key, items)
                if key in ("body", "nodes"):
                    self.nodes = getattr(self, key)
                self._children.update(i for i in items if isinstance(i, NodeBase))
            else:
                setattr(self, key, value)

    def __hash__(self):
        return hash(f"{self.nodeType}{self.depth}{self.offset}")

    def __repr__(self):
        repr_str = f"<{self.nodeType}"
        if hasattr(self, "nodes"):
            repr_str += " iterable"
        if hasattr(self, "type"):
            if type(self.type) is str:
                repr_str += f" {self.type}"
            else:
                repr_str += f" {self.type._display()}"
        if self._display():
            repr_str += f" '{self._display()}'"
        else:
            repr_str += " object"
        return f"{repr_str}>"

    def _display(self):
        if hasattr(self, "name") and hasattr(self, "value"):
            return "{} = {}".format(self.name, self.value)
        for attr in ("name", "value", "absolutePath"):
            if hasattr(self, attr):
                return f"{getattr(self, attr)}"
        return ""

    def keys(self):
        return [i for i in dir(self) if not i.startswith("_")]

    def children(
        self,
        depth=None,
        include_self=False,
        include_parents=True,
        include_children=True,
        inner_offset=None,
        outer_offset=None,
        filters={},
        exclude={},
    ):
        """Get childen nodes of this node.

        Arguments:
          depth: Number of levels of children to traverse. 0 returns only this node.
          include_self: Includes this node in the results.
          include_parents: Includes nodes that match in the results, when they also have
                        child nodes that match.
          include_children: If True, as soon as a match is found it's children will not
                            be included in the search.
          inner_offset: Only match nodes with a source offset that contains this offset.
          outer_offset: Only match nodes when their source offset is contained inside
                        this source offset.
          filters: Dictionary of {attribute: value} that children must match. Can also
                   be given as a list of dicts, children that match one of the dicts
                   will be returned.
          exclude: Dictionary of {attribute:value} that children cannot match.

        Returns:
            List of node objects."""
        if type(filters) is dict:
            filters = [filters]
        filter_fn = functools.partial(_check_filters, inner_offset, outer_offset, filters, exclude)
        find_fn = functools.partial(_find_children, filter_fn, include_parents, include_children)
        result = find_fn(find_fn, depth, self)
        if include_self or not result or result[0] != self:
            return result
        return result[1:]

    def parents(self, depth=-1, filters={}):
        """Get parent nodes of this node.

        Arguments:
            depth: Depth limit. If given as a negative value, it will be subtracted
                   from this object's depth.
            filters: Dictionary of {attribute: value} that parents must match.

        Returns: list of nodes"""
        if type(filters) is not dict:
            raise TypeError("Filters must be a dict")
        if depth < 0:
            depth = self.depth + depth
        if depth >= self.depth or depth < 0:
            raise IndexError("Given depth exceeds node depth")
        node_list = []
        parent = self
        while True:
            parent = parent._parent
            if not filters or _check_filter(parent, filters, {}):
                node_list.append(parent)
            if parent.depth == depth:
                return node_list

    def parent(self, depth=-1, filters={}):
        """Get a parent node of this node.

        Arguments:
            depth: Depth limit. If given as a negative value, it will be subtracted
                   from this object's depth. The parent at this exact depth is returned.
            filters: Dictionary of {attribute: value} that the parent must match.

        If a filter value is given, will return the first parent that meets the filters
        up to the given depth. If none is found, returns None.

        If no filter is given, returns the parent at the given depth."""
        if type(filters) is not dict:
            raise TypeError("Filters must be a dict")
        if depth < 0:
            depth = self.depth + depth
        if depth >= self.depth or depth < 0:
            raise IndexError("Given depth exceeds node depth")
        parent = self
        while parent.depth > depth:
            parent = parent._parent
            if parent.depth == depth and not filters:
                return parent
            if filters and _check_filter(parent, filters, {}):
                return parent
        return None

    def is_child_of(self, node):
        """Checks if this object is a child of the given node object."""
        if node.depth >= self.depth:
            return False
        return self.parent(node.depth) == node

    def is_parent_of(self, node):
        if node.depth <= self.depth:
            return False
        return node.parent(self.depth) == self


class IterableNodeBase(NodeBase):
    def __getitem__(self, key):
        if type(key) is str:
            try:
                return next(i for i in self.nodes if getattr(i, "name", None) == key)
            except StopIteration:
                raise KeyError(key)
        return self.nodes[key]

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, obj):
        return obj in self.nodes


def node_class_factory(ast, parent):
    if not isinstance(ast, dict) or "nodeType" not in ast:
        return ast
    name = ast["nodeType"]
    base_class = IterableNodeBase if ("nodes" in ast or "body" in ast) else NodeBase
    return type(name, (base_class,), {})(ast, parent)


def _check_filters(inner_offset, outer_offset, filters, exclude, node):
    if inner_offset and not is_inside_offset(inner_offset, node.offset):
        return False
    if outer_offset and not is_inside_offset(node.offset, outer_offset):
        return False
    for f in filters:
        if _check_filter(node, f, exclude):
            return True
    return False


def _check_filter(node, filters, exclude):
    for key, value in filters.items():
        if getattr(node, key, not value) != value:
            return False
    for key, value in exclude.items():
        if getattr(node, key, not value) == value:
            return False
    return True


def _find_children(filter_fn, include_parents, include_children, find_fn, depth, node):
    if depth is not None:
        depth -= 1
        if depth < 0:
            return [node] if filter_fn(node) else []
    if not include_children and filter_fn(node):
        return [node]
    node_list = []
    for child in node._children:
        node_list.extend(find_fn(find_fn, depth, child))
    if (include_parents or not node_list) and filter_fn(node):
        node_list.insert(0, node)
    return node_list


def is_inside_offset(inner, outer):
    """Checks if the first offset is contained in the second offset

    Args:
        inner: inner offset tuple
        outer: outer offset tuple

    Returns: bool"""
    return outer[0] <= inner[0] <= inner[1] <= outer[1]
