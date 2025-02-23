import pytest
import json
import yaml
from pathlib import Path
from unittest.mock import mock_open, patch


from caravel.parsing.Parser import Parser


@pytest.fixture
def parser():
    return Parser()

@pytest.mark.parametrize("input_text, expected", [
    ("This is a description.", "This is a description."),
    (":::info This is markdown :::", ""),
    ("Line1\n\nLine2", "Line1 Line2"),
    ("[Click here](http://example.com)", "Click here (http://example.com)")
])
def test_clean_description(parser, input_text, expected):
    assert parser._clean_description(input_text) == expected
    
def test_get_api_dictionary(parser):
    parser.api_dictionary = {"GET Users": {"path": "/v1/users/"}}
    
    assert parser.get_api_dictionary() == {"GET Users": {"path": "/v1/users/"}}
    
def test_get_api_entry(parser):
    parser.api_dictionary = {"GET Users": {"path": "/users"}}
    
    assert parser.get_api_entry("GET Users") == {"path": "/users"}
    assert parser.get_api_entry("POST Users") == "There is no valid route associated with the following intent: POST Users"

