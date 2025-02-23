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

def test_create_api_dictionary(parser):
    """Ensures OpenAPI spec is parsed correctly."""
    openapi_dict = {
        "paths": {
            "/users": {
                "get": {
                    "description": "Retrieve a list of users.",
                    "parameters": [{"name": "limit", "required": True}],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "example": {"limit": 10}
                            }
                        }
                    }
                }
            }
        }
    }

    result = parser.create_api_dictionary(openapi_dict)

    assert "GET Retrieve a list of users." in result
    assert result["GET Retrieve a list of users."]["path"] == "/users"
    assert result["GET Retrieve a list of users."]["request_example"] == {"limit": 10}
    assert result["GET Retrieve a list of users."]["required"] == ["limit"]

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"paths": {}}))
def test_extract_openapi_json(mock_file):
    """Tests if extract_openapi_json reads and parses a JSON file correctly."""
    result = Parser.extract_openapi_json("/openapi.json")
    assert result == {"paths": {}}
    mock_file.assert_called_once_with(f"{Path.cwd()}/openapi.json", "r")
    
@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load", return_value={"openapi": "3.0.0"})
def test_make_openapi_json(mock_yaml_load, mock_file):
    """Tests if make_openapi_json correctly converts YAML to JSON."""
    Parser.make_openapi_json("/openapi.yaml", "/openapi.json", indent=2)

    # Ensure yaml.safe_load was called
    mock_yaml_load.assert_called_once()
    # Ensure the file was written to
    mock_file.assert_called_with(f"{Path.cwd()}/openapi.json", "w")