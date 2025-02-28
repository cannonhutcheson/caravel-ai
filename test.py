from src.caravel.baml.Runner import BamlRunner
from src.caravel.parsing.Parser import Parser
from src.caravel.http.Client import Client
import asyncio
# import json
# from src.caravel.baml.baml_client import b
# from src.caravel.baml.baml_client import reset_baml_env_vars


# import os
# import dotenv

# dotenv.load_dotenv()
# reset_baml_env_vars(dict(os.environ))

        
        
async def new_main():
       
    parser = Parser()
    json_dict = parser.json_to_dict("samsara.json")
    parser.set_openapi_spec(json_dict)
    parser.map_paths_to_desc(parser.openapi_spec)
    # print(parser.path_map.keys())
    runner = BamlRunner(parser)
    
    
    while True:
        user_prompt = input("What can I help you with today? \n ---------------------------- \n $ ")

        api_request = await runner.construct_api_request(intents=list(parser.path_map.keys()), user_prompt=user_prompt)
        client = Client(
            name="Test Client",
            base_url="http://localhost:4010",
            auth_headers={
                "Accept": "application/json",
                "Authorization": f"Bearer dummy-token",
                # "Account-Token": "dummy-acct-id"
                # "X-Api-Version": "2024-06-30"
            },
            allowed_methods=["get", "post", "patch", "delete", "put"]
            )
        response = None
        if api_request.method == "GET":
            try:
                response = await client.get(api_request)
            except Exception as e:
                print(f"GET: The following error occured: {e}")
            
        elif api_request.method == "POST":
            try:
                response = await client.post(api_request)
            except Exception as e:
                print(f"POST: The following error occured: {e}")        
        elif api_request.method == "DELETE":
            try:
                response = await client.delete(api_request)
            except Exception as e:
                print(f"DELETE: The following error occured: {e}")
            
        elif api_request.method == "PATCH":
            try:
                response = await client.patch(api_request)
            except Exception as e:
                print(f"PATCH: The following error occured: {e}")
            
        elif api_request.method == "PUT":
            try:
                response = await client.put(api_request)
            except Exception as e:
                print(f"PUT: The following error occured: {e}") 
        
        print(response)                
                


if __name__ == "__main__":
    asyncio.run(new_main())
