import json
import yaml
from pathlib import Path
import re

class Parser:
    def __init__(self):
        self.api_dictionary = dict()

    def _clean_description(desc):
        '''
        Cleans up the OpenAPI description by removing unwanted markdown formatting.
        '''
        if not desc:
            return "N/A"
        
        desc = re.sub(r":::.*?:::", "", desc, flags=re.DOTALL)
        desc = re.sub(r"\n{2,}", " ", desc).strip()
        desc = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", desc)
        return desc

    def create_api_dictionary(self, openapi_dict, cleanup_markdown=True, first_sentence=True, reformat=False):
        '''
        Parses an OpenAPI JSON Spec and extracts key details for each path.
        
        Args:
            openapi_json (dict): The OpenAPI spec as a dict.
        
        Returns:
            dict: A dictionary with paths as keys and the other info as values.
        '''

        parsed_data = dict()
        paths = openapi_dict.get("paths", {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                # Only concerned with CRUD ops
                if method not in ["get", "post", "put", "delete", "patch"]:
                    continue
                
                # Extraction
                description = details.get("description", "N/A")
                required = []
                request_example = None
                
                
                parameters = details.get("parameters", [])
                for param in parameters:
                    if param.get("required", False):
                        required.append(param["name"])
                
                request_body = details.get("requestBody", {})
                content = request_body.get("content", {})
                if "application/json" in content:
                    examples = content["application/json"].get("example") or content["application/json"].get("examples", {})
                    request_example = examples if examples else None
                
                if cleanup_markdown:          
                    description = self._clean_description(description)
                if first_sentence:
                    description = description.split(".")[0] + "."
                if reformat:
                    raise Exception("LLM Description Reformatting has not yet been implemented.")
            
                if parsed_data.get(f"{description}", False):
                    raise Exception("This key is already here.")
                            
                parsed_data[f"{description}"] = {
                    "path": path,
                    "request_example": request_example,
                    "required": required
                } # parsed_data
                        
        self.api_dictionary = parsed_data
        return parsed_data
    
    def get_api_dictionary(self):
        '''
        Returns the entire API dictionary.
        '''
        return self.api_dictionary

    def get_api_entry(self, intent: str):
        '''
        Returns a single entry from the API Dictionary.
        '''
        return self.api_dictionary.get(intent, f"There is no valid route associated with the following intent: {intent}")
        
    
    @staticmethod
    def extract_openapi_json(path):
        '''
        Extracts the openapi json from the json file, converts it to a dict, and returns it.
        '''
        with open(f"{Path.cwd()}{path}", "r") as f:
            openapi_dict = json.load(f)
        return openapi_dict
    
    @staticmethod
    def make_openapi_json(yamlpath: str, jsonpath: str, indent:int=0):
        '''
        Converts an OpenAPI YAML file to an OpenAPI JSON file.
        
        Args:
            yamlpath (str): Path to the input YAML file.
            jsonpath (str): Path to the output JSON file. 
        '''
        with open(f"{Path.cwd()}{yamlpath}", "r") as yml:
            yaml_data = yaml.safe_load(yml)
        with open(f"{Path.cwd()}{jsonpath}", "w") as jsn:
            json.dump(yaml_data, jsn, indent=indent)
