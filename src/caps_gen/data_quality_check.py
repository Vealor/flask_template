from anytree import Node

#===============================================================================
# Map datatype to regex for data quality check
def map_regex(dt_type):
    regex = ''
    if dt_type == 'dt_varchar':
        regex = r'.*'
    elif dt_type == 'dt_float':
        regex = r'^(?:\-)?\d*\.{1}\d+$'
    elif dt_type == 'dt_int':
        regex = r'^(?:\-)?\d+$'
    elif dt_type == 'dt_date':
        regex = r'^(0[1-9]|1[012])\/(0[1-9]|[1-2][0-9]|3[01])\/\d{4}$'
    else:
        raise Exception('No regex implmented for the given data type: {}'.format(dt_type))
    return regex

#===============================================================================
# Recursion helper for data quality check
def recursive_insert(root: Node, sub_str):
    char = sub_str[0]
    flag = False
    if root.children:
        for child in root.children:
            if char == child.name:
                if len(sub_str) > 1:
                    recursive_insert(child, sub_str[1:])
                else:
                    child.count += 1
                flag = True
    elif not flag:
        new_node = Node(char, parent=root, count=0)
        if len(sub_str) > 1:
            recursive_insert(new_node, sub_str[1:])
        else:
            new_node.count += 1

def recursive_find(root: Node, sub_str):
    char = sub_str[0]
    if root.children:
        for child in root.children:
            if char == child.name:
                if len(sub_str) > 1:
                    return recursive_find(child, sub_str[1:])
                else:
                    if child.count > 0:
                        return True
    return False
