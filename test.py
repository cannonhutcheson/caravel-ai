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

        
        
async def new_main():
       
    parser = Parser()
    json_dict = parser.json_to_dict("output.json")
    parser.set_openapi_spec(json_dict)
    parser.map_paths_to_desc(parser.openapi_spec)
    print(parser.path_map.keys())
    runner = BamlRunner(parser)
    
    api_request = await runner.construct_api_request(intents=list(parser.path_map.keys()), user_prompt="I want to upload a new vehicle to fleetio. Name it cannons truck, status_id of 2, type id of 3, and primary meter unit of miles")
    print(api_request)
    
if __name__ == "__main__":
    asyncio.run(new_main())
