#!/usr/bin/python3


def get_node_objects(node, node_type, class_, parent):
    result = [i for i in node['nodes'] if i['nodeType'] == node_type]
    for i in result:
        node['nodes'].remove(i)
    return [class_(i, parent) for i in result]
