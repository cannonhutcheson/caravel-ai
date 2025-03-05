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


from src.caravel.baml.Runner import BamlRunner
from src.caravel.parsing.SchemaAdder import SchemaAdder, parse_json_schema
from src.caravel.parsing.Parser import Parser
from caravel.baml.baml_client.type_builder import TypeBuilder
from caravel.baml.baml_client import b
import json
import time
        
async def new_main():
       
    # parser = Parser()
    # json_dict = parser.json_to_dict("samsara.json")
    # parser.set_openapi_spec(json_dict)
    # parser.map_paths_to_desc(parser.openapi_spec)
    parser = Parser(file="samsara.json")
    runner = BamlRunner(parser)
    
    
    while True:
        user_prompt = input("What can I help you with today? \n ---------------------------- \n $ ")
        start_time1 = time.time()
        api_request = await runner.construct_dynamic_api_request(intents=list(parser.path_map.keys()), context=user_prompt)
        print(f"API Request to be submitted: {api_request}")
        end_time1 = time.time()
        keep_going = input("Y to proceed, N to end: \n$ ")
        if keep_going.lower() == "n":
            continue
        start_time2 = time.time()
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
        
        # can be toggled when fleetio api is being mocked on port 4010
        # client = Client(
        #     name="Test Client",
        #     base_url="http://localhost:4010",
        #     auth_headers={
        #         "Accept": "application/json",
        #         "Authorization": f"Token dummy-token",
        #         "Account-Token": "dummy-acct-id",
        #         "X-Api-Version": "2024-06-30"
        #     },
        #     allowed_methods=["get", "post", "patch", "delete", "put"]
        #     )
        
        
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
        
        hl_response = await b.GenerateHumanLanguageResponse(json.dumps(response), user_prompt)
        print(hl_response)
        end_time2 = time.time()
        
        print(f"D1: {end_time1 - start_time1}")
        print(f"D2: {end_time2 - start_time2}")
        print(f"Total time: {(end_time1 - start_time1) + (end_time2 - start_time2)}")        


if __name__ == "__main__":
    asyncio.run(new_main())
