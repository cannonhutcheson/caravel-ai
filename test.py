from src.caravel.baml.Runner import BamlRunner
from src.caravel.parsing.Parser import Parser
from src.caravel.http.Client import Client
import asyncio
import json
from src.caravel.baml.baml_client import b
from src.caravel.baml.baml_client import reset_baml_env_vars

import os
import dotenv

dotenv.load_dotenv()
reset_baml_env_vars(dict(os.environ))

async def main():
    # create a Parser
    parser = Parser()
    # create a BamlRunner and link it with a parser
    runner = BamlRunner(parser)
    # create a Client
    client = Client("Test client", base_url="http://localhost:3000", allowed_methods=["get", "post", "patch", "put", "delete"])


    # turning the spec into a dict
    my_spec = runner.parser.make_openapi_json("/2024-06-30.yaml", "/open_api.json")
    spec_as_dict = runner.parser.extract_openapi_json("/open_api.json")

    # creating the API dictionary
    runner.parser.create_api_dictionary(spec_as_dict)

    # getting the API dictionary
    api_dict = runner.parser.get_api_dictionary()
    print("API DICT: ", api_dict)
    
    # getting intent from the runner.
    intent = await runner.get_intent(list(api_dict.keys()), intent="I want to post a new vehicle to fleetio.")
    
    # getting the path from the api dictionary 
    endpoint = runner.parser.get_api_entry(intent)["path"]
    print(endpoint)

    print("Request Example: ", runner.parser.get_api_entry(intent)['request_example'])
    print("Required: ", runner.parser.get_api_entry(intent)['required'])
    
    body_structure = await runner.get_request_body(str(f"{runner.parser.get_api_entry(intent)['request_example'], runner.parser.get_api_entry(intent)['required']}"))
    
    print(body_structure)


    
    
if __name__ == "__main__":
    asyncio.run(main())
