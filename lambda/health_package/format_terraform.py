"""Utility functions to generate output in the form of a tfvars file"""
from logger import LOG


def get_tf_map(source, indent_size, indent_level=0):
    """Turn dict object into a tf map"""
    outer_line_prefix = "".rjust(indent_level * indent_size)
    inner_line_prefix = "".rjust((indent_level + 1) * indent_size)
    formatted = "{\n"
    tf_items = []
    for key in source:
        item = get_tf_item(source[key], indent_size, indent_level)
        tf_item = f"{inner_line_prefix}{key} = {item}"
        tf_items.append(tf_item)
    formatted += ",\n".join(tf_items) + "\n"
    formatted += outer_line_prefix + "}"
    return formatted


def get_tf_list(source, indent_size, indent_level=0):
    """Turn list into a tf list"""
    outer_line_prefix = "".rjust(indent_level * indent_size)
    inner_line_prefix = "".rjust((indent_level + 1) * indent_size)
    formatted = "[\n"
    tf_items = []
    for item in source:
        tf_item = inner_line_prefix + get_tf_item(item, indent_size, indent_level)
        tf_items.append(tf_item)
    formatted += ",\n".join(tf_items) + "\n"
    formatted += outer_line_prefix + "]\n"
    return formatted


def get_tf_item(source, indent_size, indent_level=0):
    """
    Format list item or dict value depending on data type
    """
    formatted = ""
    if isinstance(source, dict):
        formatted += get_tf_map(source, indent_size, indent_level + 1)
    elif isinstance(source, list):
        formatted += get_tf_list(source, indent_size, indent_level + 1)
    elif isinstance(source, str):
        formatted += f'"{source}"'
    elif isinstance(source, int):
        formatted += f"{source}"
    elif isinstance(source, float):
        formatted += f"{source}"
    elif source is None:
        formatted += '""'
    else:
        LOG.warn(str(type(source)))
    return formatted
