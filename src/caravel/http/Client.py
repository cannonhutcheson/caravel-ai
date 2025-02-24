from typing import Callable, Dict
from src.caravel.registry.CaravelRegistry import CaravelRegistry
import json
import httpx

class Client:
    def __init__(self, name: str, base_url: str, auth_headers: dict={}, allowed_methods=["get", "post"], restricted_routes=[]):
        self.name = name
        self.base_url=base_url
        self.auth_headers=auth_headers
        self.allowed_methods=allowed_methods
        self.restricted_routes=restricted_routes
        self.functions: Dict[str, Callable] = {} # allows users to add util functions.

    def set_auth_headers(self, auth_headers:dict={}):
        self.auth_headers = auth_headers
        
    def get_auth_headers(self):
        return self.auth_headers
    
    def get_base_url(self):
        return self.base_url

    @CaravelRegistry.register(is_async=True)    
    async def post(self, route:str, params:str):    
        if "post" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
        params = json.loads()
         

    
    # TODO: figure out typing for params
    @CaravelRegistry.register(is_async=True)
    async def get_all(self, route, params, custom_error=None):
        try:
            if "get" not in self.allowed_methods:
                return
            if route in self.restricted_routes:
                return
            with httpx.AsyncClient as client:
                response = await client.get(
                    f"{self.get_base_url()}{route}",
                    params=params,
                    headers=self.get_auth_headers()
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return f"The API request to the route {route} failed with exception {e}"

    
    @CaravelRegistry.register(is_async=True)
    async def get(self, route, params):
        if "get" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return 
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{route}",
                    params=params,
                    headers=self.get_auth_headers()
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return f"There was an issue trying to make the API Request: {e}"
        
        
    @CaravelRegistry.register(is_async=True)
    async def patch(self, route, params):
        if "patch" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
        pass
    
    @CaravelRegistry.register(is_async=True)
    async def put(self, route, params):
        if "put" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
    
    @CaravelRegistry.register(is_async=True)
    async def delete(self, route):
        if "delete" not in self.allowed_methods:
            return
        if route not in self.restricted_routes:
            return
        pass
            
    def add_function(self, name: str, func: Callable, is_async: bool = False):
        self.functions[name] = func
        CaravelRegistry.register(instance=self, custom_name=name, is_async=is_async)
    
    def call_function(self, name: str, *args, **kwargs):
        """Call a stored function by name, first checking instance-specific and then default functions."""
        if name in self.functions:
            return self.functions[name](*args, **kwargs)
        elif hasattr(self, name):  # Check default methods
            return getattr(self, name)(*args, **kwargs)
        raise ValueError(f"Function '{name}' not found")

    def list_added_functions(self):
        return list(self.functions.keys())
    