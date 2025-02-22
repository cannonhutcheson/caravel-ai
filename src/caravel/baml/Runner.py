import json
from baml_client.async_client import b
from baml_client.types import APIRequest, RequestBody
from baml_client import reset_baml_env_vars
import os
import dotenv
dotenv.load_dotenv()
reset_baml_env_vars(dict(os.environ))

async def get_request_body(raw_json: str) -> RequestBody:
    response = await b.ExtractRequestBodySchema(raw_json)
    return response

async def make_api_request_body(schema: RequestBody, user_prompt: str) -> APIRequest:
    response = await b.CreateAPIRequestBody(schema, user_prompt)
    return response

async def get_intent(intents: list[str], intent) -> str:
    response = await b.GetIntent(intents, intent)
    return response

async def construct_api_request(user_prompt: str) -> str:
    try:
        intent = await get_intent(list(desc_to_route.keys()),   user_prompt)
        endpoint = desc_to_route[intent]
        body_structure = await get_request_body (route_to_request_params [desc_to_route[intent]])
        request_body = await make_api_request_body  (body_structure, user_prompt)
        request_body_json = json.loads(request_body.json())
        spread_params = request_body_json["params"]

        api_request_body = {
            "path": endpoint,
            "params": json.dumps(spread_params)
        } # api_request_body

        print("API Request:",   api_request_body)    
        return api_request_body
    except Exception as e:
        print(e)
        return "There was an error."