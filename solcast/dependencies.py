#!/usr/bin/python3


def set_dependencies(source_nodes):
    '''Sets contract node dependencies.

    Arguments:
        source_nodes: list of SourceUnit objects.

    Returns: SourceUnit objects where all ContractDefinition nodes contain
             'dependencies' and 'libraries' attributes.'''
    symbol_map = get_symbol_map(source_nodes)
    contract_list = [x for i in source_nodes for x in i if x.nodeType == "ContractDefinition"]

    # add immediate dependencies
    for contract in contract_list:
        contract.dependencies = set()
        contract.libraries = dict((
            _get_type_name(i.typeName),
            i.libraryName.name
        ) for i in contract.nodes if i.nodeType == "UsingForDirective")

        # listed dependencies
        for key in contract.contractDependencies:
            contract.dependencies.add(symbol_map[key])

        # using .. for libraries
        for node in contract.children(filters={'nodeType': "UsingForDirective"}):
            id_ = node.libraryName.referencedDeclaration
            contract.libraries[_get_type_name(node.typeName)] = symbol_map[id_]
            contract.dependencies.add(symbol_map[id_])

        # unlinked libraries
        for node in contract.children(filters={'node_type': "Identifier"}):
            if node.reference in symbol_map and symbol_map[node.reference].type == "library":
                contract.dependencies.add(symbol_map[node.reference])

    # add recursive dependencies
    for contract in contract_list:
        for node in contract.dependencies.copy():
            contract.dependencies |= node.dependencies

    # convert dependency sets to lists
    for contract in contract_list:
        contract.dependencies = sorted(contract.dependencies, key=lambda k: k.name)
    return source_nodes


def get_symbol_map(source_nodes):
    '''Generates a dict of {'id': SourceUnit} used for linking nodes.

    Arguments:
        source_nodes: list of SourceUnit objects.'''
    symbol_map = {}
    for node in source_nodes:
        symbol_map.update((v[0], node[k]) for k, v in node.exportedSymbols.items())
    return symbol_map


def _get_type_name(node):
    if node is None:
        return None
    if hasattr(node, 'name'):
        return node.name
    if hasattr(node, 'typeDescriptions'):
        return node.typeDescriptions.typeString
    return None
