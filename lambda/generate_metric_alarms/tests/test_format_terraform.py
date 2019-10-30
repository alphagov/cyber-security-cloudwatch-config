"""Test format_terraform module"""
import pytest

import format_terraform


@pytest.mark.usefixtures("tf_map_indent2_level0")
def test_get_tf_map(tf_map_indent2_level0):
    """Test creation of string with indent"""
    source = {
        "key1": "value1",
        "key2": "value2"
    }
    tf_item = format_terraform.get_tf_map(source, indent_size=2, indent_level=0)
    assert tf_item == tf_map_indent2_level0


@pytest.mark.usefixtures("tf_list_indent4_level0")
def test_get_tf_list(tf_list_indent4_level0):
    """Test creation of string with indent"""
    source = [
        "value1",
        "value2"
    ]
    tf_item = format_terraform.get_tf_list(source, indent_size=4, indent_level=0)
    assert tf_item == tf_list_indent4_level0
