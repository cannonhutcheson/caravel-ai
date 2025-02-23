
import json
from src.caravel.baml.baml_client.async_client import b
from src.caravel.baml.baml_client.types import APIRequest, RequestBody
from src.caravel.parsing import Parser
import os
import dotenv
dotenv.load_dotenv()
from src.caravel.baml.baml_client import reset_baml_env_vars
reset_baml_env_vars(dict(os.environ))

class BamlRunner:

    def __init__(self, parser: Parser):
        self.parser = parser
        
    
    @staticmethod
    async def get_request_body(raw_json: str) -> RequestBody:
        response = await b.ExtractRequestBodySchema(raw_json)
        return response

    @staticmethod
    async def make_api_request_body(schema: RequestBody, user_prompt: str) -> APIRequest:
        response = await b.CreateAPIRequestBody(schema, user_prompt)
        return response

    @staticmethod
    async def get_intent(intents: list[str], intent) -> str:
        response = await b.GetIntent(intents, intent)
        return response

    async def construct_api_request(self, user_prompt: str) -> str:
        try:
            intent = await self.get_intent(list(self.parser.get_api_dictionary().keys()), user_prompt)
            endpoint = self.parser.get_api_entry[intent]["path"]
            body_structure = await self.get_request_body({self.parser.get_api_entry(intent)["request_example"], self.parser.get_api_entry(intent)["required"]})
            request_body = await self.make_api_request_body(body_structure, user_prompt)
            request_body_json = json.loads(request_body.json())
            spread_params = request_body_json["params"]

            api_request_body = {
                "path": endpoint,
                "params": json.dumps(spread_params)
            } # api_request_body

            # print("API Request:", api_request_body)    
            return api_request_body
        except Exception as e:
            print(e)
            return "There was an error."

