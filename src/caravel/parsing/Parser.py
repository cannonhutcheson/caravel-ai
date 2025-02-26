import json
import ruamel.yaml
from pathlib import Path
import re

class Parser:
    def __init__(self):
        self.api_dictionary = dict()
        self.path_map = dict()
    def _clean_markdown(self, desc):
        '''
        Cleans up the OpenAPI description by removing unwanted markdown formatting.
        '''
        if not desc:
            return "N/A"
        
        desc = re.sub(r":::.*?:::", "", desc, flags=re.DOTALL)
        desc = re.sub(r"\n{2,}", " ", desc).strip()
        desc = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", desc)
        return desc


    def yaml_to_json(self, in_file: str, out_file: str) -> None:
        yml = ruamel.yaml.YAML(typ='safe')
        with open(in_file) as fpi:
            data = yml.load(fpi)
        with open(out_file, 'w') as fpo:
            json.dump(data, fpo, indent=2)

    def json_to_dict(self, in_file: str) -> dict: 
        with open(in_file) as f:
            return json.loads(f)
    
    # make a more generic signature here
    
    def map_paths_to_desc(self, openapi_spec: dict) -> dict:
        
        for path, methods in openapi_spec["paths"].items():
            for method, details in methods.items():
                desc = details.get("summary", details.get("description", path))

                desc = self._clean_markdown(desc)
                formatted_key = f"{method.upper()} {desc}"

                self.path_map[formatted_key] = path
                
        return self.path_map
    
    
    
    def resolve_ref(self, ref_path: str) -> dict:
        keys = ref_path.lstrip("#/").split("/")
        schema = self.openapi_spec
        
        for key in keys:
            schema = schema.get(key, {})
            
        if "$ref" in schema:
            return self.resolve_ref(schema["$ref"], self.openapi_spec)
        
        return schema

    def extract_query_param_defaults(self, path: str, method: str) -> dict:
        query_param_defaults = {}
        
        query_params_schema = [
            p for p in self.openapi_spec["paths"][path][method]["parameters"] if p["in"] == "query"
        ]
        
        def get_default_value(schema):
            
            if "$ref" in schema:
                schema = self.resolve_ref(schema["$ref"], self.openapi_spec)
                
            if "enum" in schema:
                return " | ".join(schema["enum"])
            
            if "oneOf" in schema:
                # resolved_options = [resolve_ref(option["$ref"], openapi_spec) for option in schema["oneOf"]]
                # return {"oneOf": resolved_options}
                possible_keys = []
                for option in schema["oneOf"]:
                    resolved = self.resolve_ref(option["$ref"], self.openapi_spec) if "$ref" in option else option
                    if "properties" in resolved:
                        possible_keys.extend(resolved["properties"].keys())
                return possible_keys
            
            if "default" in schema:
                return schema["default"]            
            
            schema_type = schema.get("type")
            print(f"{schema_type}")
            if schema_type == "string":
                return "<string>"
            elif schema_type == "integer":
                return 0 # needs to be @ least 1 for pagination
            elif schema_type == "boolean":
                return [True, False]
            elif schema_type == "number":
                return 0.0
            elif schema_type == "array":
                return ["<array>"]
            elif schema_type == "object":
                return {
                    key: get_default_value(value) for key, value in schema.get("properties", {}).items()
                }
            return None
        
        # populating
        for param in query_params_schema:
            name = param["name"]
            schema = param.get("schema", {})
            # query_param_defaults[name] = get_default_value(schema)
            possible_vals = get_default_value(schema)
            ### handle oneOf here
            if "oneOf" in schema:
                query_param_defaults[name] = " | ".join(possible_vals)
            else:
                query_param_defaults[name] = possible_vals
            
            
        return query_param_defaults


    def flatten_query_params(self, params: dict, prefix: str="") -> dict:
        flat_params = {}
        for key, value in params.items():
            full_key = f"{prefix}[{key}]" if prefix else key
            
            if isinstance(value, dict):
                flat_params.update(self.flatten_query_params(value, full_key))
            elif isinstance(value, list):
                flat_params[full_key] = " | ".join(map(str, value))
            else:
                flat_params[full_key] = value
                
        return flat_params

    
    


# LEGACY -------------------------------
#     def create_api_dictionary(self, openapi_dict, cleanup_markdown=True, first_sentence=True, reformat=False):
#         # print(openapi_dict)
#         # print(openapi_dict.keys())
#         # print(openapi_dict.get("paths"))
#         for path, methods in openapi_dict.get("paths", {}).items():
#             print("Path: ", path)
#             for method, details in methods.items():
#                 print("method: ", method)
#                 if method.lower() not in ["put", "patch", "get", "post", "delete"]:
#                     continue
                
#                 # this will get query & path params
#                 pq_params = methods.get("parameters", [])
                
#                 description = details.get("description", "N/A").strip()
#                 print("Description: ", description)
                
#                 description = self._clean_markdown(desc=description).split(".")[0] + '.'
#                 print("Cleaned description: ", description)
                
#                 request_example = None
#                 required_params = []
#                 required_req = []
#                 properties={}
#                 print("example and required inited: ", request_example, required_params)
                
#                 if "requestBody" in details:
#                     print("requestBody found in details")
#                     content = details["requestBody"].get("content", {})
#                     print("content from requestBody: ", content)
#                     if "application/json" in content:
#                         print("application/json present in content")
#                         example_data = content["application/json"].get("example")
#                         examples_data = content["application/json"].get("examples", {}).values()

#                         if example_data:
#                             print("Example data:", example_data)
#                             request_example = example_data
#                         elif examples_data:
#                             print("Example data", examples_data[0].get("value"))
#                             request_example = examples_data[0].get("value")

#                         properties = content["application/json"].get('schema', {}).get("properties", {})
                        
#                         required_req = content["application/json"].get("schema", {}).get("required", [])
                        
#                 if "parameters" in details:
#                     print('"parameters" in details')
#                     required_params = [
#                         param["name"] for param in details["parameters"] if param.get("required", False)
#                     ]
#                     print("required params: ", required_params)
#                 key = f"{method.upper()} {description}"
#                 self.api_dictionary[key] = {
#                     "path": path,
#                     "parameters": pq_params,
#                     "properties": properties,
#                     "request_example": request_example,
#                     "required": required_params,
#                     "required_req": required_req
#                 }
#         return "Success"

# # NEELS code
#     # def create_api_dictionary_from_json(self, openapi_dict, cleanup_markdown=True, first_sentence=True, reformat=False):
#     #     '''
#     #     Parses an OpenAPI JSON Spec and extracts key details for each path.
        
#     #     Args:
#     #         openapi_json (dict): The OpenAPI spec as a dict.
        
#     #     Returns:
#     #         dict: A dictionary with paths as keys and the other info as values.
#     #     '''

#     #     parsed_data = dict()
#     #     paths = openapi_dict.get("paths", {})
        
#     #     for path, methods in paths.items():
#     #         for method, details in methods.items():
#     #             # Only concerned with CRUD ops
#     #             if method not in ["get", "post", "put", "delete", "patch"]:
#     #                 continue
                
#     #             # Extraction
#     #             description = details.get("description", "N/A")
#     #             required = []
#     #             request_example = None
                
                
#     #             parameters = details.get("parameters", [])
#     #             if parameters:
#     #                 print("PARAM:", parameters)
#     #             for param in parameters:
#     #                 if param.get("required", False):
#     #                     required.append(param["name"])
                
#     #             request_body = details.get("requestBody", {})
#     #             if request_body:
#     #                 print("REQ:",request_body)
#     #             content = request_body.get("content", {})
#     #             if "application/json" in content:
#     #                 examples = content["application/json"].get("example") or content["application/json"].get("examples", {})
#     #                 request_example = examples if examples else None
                
#     #             if cleanup_markdown:          
#     #                 description = self._clean_description(description)
#     #             if first_sentence:
#     #                 description = description.split(".")[0] + "."
#     #             if reformat:
#     #                 raise Exception("LLM Description Reformatting has not yet been implemented.")
            
#     #             if parsed_data.get(f"{description}", False):
#     #                 raise Exception("This key is already here.")
                            
#     #             parsed_data[f"{method.upper()} {description}"] = {
#     #                 "path": path,
#     #                 "request_example": request_example,
#     #                 "required": required
#     #             } # parsed_data
                        
#     #     self.api_dictionary = parsed_data
#     #     return parsed_data
        
#     # def get_schema_properties(self, ref_path, yaml_data, visited_refs=None):
        
#     #     if visited_refs is None:
#     #         visited_refs = set()

#     #     if not isinstance(ref_path, str) or not ref_path.startswith("#/ components/schemas/"):
#     #         return {"error": "Invalid $ref path"}

#     #     schema_name = ref_path.rsplit("/", 1)[-1]

#     #     if schema_name in visited_refs:
#     #         return {"error": "Circular reference detected", "schema":   schema_name}

#     #     while True:
#     #         if schema_name in visited_refs:
#     #             return {"error": "Circular reference detected", "schema":   schema_name}

#     #         visited_refs.add(schema_name)
#     #         schema = yaml_data.get("components", {}).get("schemas", {}).    get(schema_name)

#     #         if not isinstance(schema, dict):
#     #             return {"schema": schema_name, "properties": "No    properties found"}

#     #         if "properties" in schema:
#     #             return {"schema": schema_name, "properties": schema ["properties"]}

#     #         ref_path = schema.get("$ref")
#     #         if not ref_path:
#     #             return {"schema": schema_name, "properties": "No    properties found"}

#     #         schema_name = ref_path.rsplit("/", 1)[-1]
    
    
#     # def extract_yaml(self, api_dict = {}, yaml_data = None):
#     #     for path, methods in yaml_data.get("paths", {}).items():
#     #         for method, details in methods.items():
#     #             method_upper = method.upper()  # Convert HTTP method to     uppercase

#     #             if method_upper not in api_dict:
#     #                 api_dict[method_upper] = {}

#     #             # Initialize API path entry
#     #             api_dict[method_upper][path] = {
#     #                 "description": details.get("description", "No   description available"),
#     #                 "request_body_example": None  # Default value for   request body
#     #             }

#     #             # Check for request body example (for POST and PATCH    requests)
#     #             if method_upper in ["POST", "PUT", "PATCH", "DELETE"] and   "requestBody" in details:
#     #                 content = details["requestBody"].get("content", {})
#     #                 if "required" in content["application/json"]    ["schema"].keys():
#     #                     # print(content["application/json"]["schema"]   ["required"])
#     #                     api_dict[method_upper][path]["required"] = content  ["application/json"]["schema"]["required"]
#     #                 if "properties" in content["application/json"]  ["schema"].keys():
#     #                     api_dict[method_upper][path]    ["request_body_example"] = content["application/    json"]["schema"]["properties"]
#     #                 elif "$ref" in content["application/json"]["schema"].   keys() and "properties" not in content["application/   json"]["schema"].keys():
#     #                     properties = self.get_schema_properties(content  ["application/json"]["schema"]["$ref"],   yaml_data=yaml_data)
#     #                     api_dict[method_upper][path]    ["request_body_example"] = properties

#     #                 for content_type, content_details in content.items():
#     #                     # Check if 'example' is directly provided
#     #                     if "requestBody" in content_details:
#     #                         api_dict[method_upper][path]    ["request_body_example"] = content_details  ["requestBody"]
#     #                     # Check inside 'schema' for an example
#     #                     elif "schema" in content_details and "example" in   content_details["schema"]:
#     #                         api_dict[method_upper][path]    ["request_body_example"] = content_details  ["schema"]["example"]

#     #     return api_dict   
# ###

#     def get_api_dictionary(self):
#         '''
#         Returns the entire API dictionary.
#         '''
#         return self.api_dictionary

#     def get_api_entry(self, intent: str):
#         '''
#         Returns a single entry from the API Dictionary.
#         '''
#         return self.api_dictionary.get(intent, f"There is no valid route associated with the following intent: {intent}")
        
    
#     @staticmethod
#     def extract_openapi_json(path):
#         '''
#         Extracts the openapi json from the json file, converts it to a dict, and returns it.
#         '''
#         with open(f"{Path.cwd()}{path}", "r") as f:
#             openapi_dict = json.load(f)
#         return openapi_dict
    
#     @staticmethod
#     def make_openapi_json(yamlpath: str, jsonpath: str, indent:int=0):
#         '''
#         Converts an OpenAPI YAML file to an OpenAPI JSON file.
        
#         Args:
#             yamlpath (str): Path to the input YAML file.
#             jsonpath (str): Path to the output JSON file. 
#         '''
#         with open(f"{Path.cwd()}{yamlpath}", "r") as yml:
#             yaml_data = yaml.safe_load(yml)
#         with open(f"{Path.cwd()}{jsonpath}", "w") as jsn:
#             json.dump(yaml_data, jsn, indent=indent)
