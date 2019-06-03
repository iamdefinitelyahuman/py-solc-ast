#!/usr/bin/python3


def get_symbol_map(source_nodes):
    '''Generates a dict of {'id': SourceUnit} used for linking nodes.

    Arguments:
        source_nodes: list of SourceUnit objects.'''
    symbol_map = {}
    for node in source_nodes:
        symbol_map.update((v[0], node[k]) for k, v in node._node['exportedSymbols'].items())
    return symbol_map


def get_node_objects(node, node_type, class_, parent):
    '''Creates node objects from a list of nodes.

    Arguments:
        node: list of nodes from AST dict.
        node_type: generate objects of this type.
        class_: python class to instantiate.
        parent: parent node of new objects.

    Returns: list of node objects'''
    result = [i for i in node['nodes'] if i['nodeType'] == node_type]
    for i in result:
        node['nodes'].remove(i)
    return [class_(i, parent) for i in result]


def is_inside_offset(inner, outer):
    '''Checks if the first offset is contained in the second offset

    Args:
        inner: inner offset tuple
        outer: outer offset tuple

    Returns: bool'''
    return outer[0] <= inner[0] <= inner[1] <= outer[1]
