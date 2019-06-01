#!/usr/bin/python3


def get_symbol_map(source_nodes):
    '''Generates a dict of {'id': SourceUnit} used for linking nodes.

    Arguments:
        source_nodes: list of SourceUnit objects.'''
    symbol_map = {}
    for node in source_nodes:
        symbol_map.update((v[0], node[k]) for k, v in node._node['exportedSymbols'].items())
    return symbol_map


def set_dependencies(source_nodes):
    '''Sets contract node dependencies.

    Arguments:
        source_nodes: list of SourceUnit objects.

    Returns: SourceUnit objects where all ContractDefinition nodes contain
             'dependencies' and 'libraries' attributes.'''
    symbol_map = get_symbol_map(source_nodes)

    # add immediate dependencies
    for contract in [x for i in source_nodes for x in i]:
        contract.dependencies = set()

        # listed dependencies
        for key in contract._node['contractDependencies']:
            contract.dependencies.add(symbol_map[key])

        # using .. for libraries
        for node in [i for i in contract._node['nodes'] if i['nodeType'] == "UsingForDirective"]:
            contract._node['nodes'].remove(node)
            id_ = node['libraryName']['referencedDeclaration']
            contract.libraries[node['typeName']['name']] = symbol_map[id_]
            contract.dependencies.add(symbol_map[id_])

        # unlinked libraries
        for node in contract.children(filters={'node_type': "Identifier"}):
            if node.reference in symbol_map and symbol_map[node.reference].type == "library":
                contract.dependencies.add(symbol_map[node.reference])

    # add recursive dependencies
    for contract in [x for i in source_nodes for x in i]:
        for node in contract.dependencies.copy():
            contract.dependencies |= node.dependencies

    # convert dependency sets to lists
    for contract in [x for i in source_nodes for x in i]:
        contract.dependencies = sorted(contract.dependencies, key=lambda k: k.name)
    return source_nodes


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
