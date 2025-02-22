from typing import Dict, Any, Callable

class Registry:
    functions = {}
    @classmethod
    def register(cls, custom_name=None, is_async=False):
        def decorator(func: Callable):
            name = custom_name or func.__name__
            cls.functions[name] = [func, is_async]
            return func    
        return decorator
    @classmethod
    def get_function(cls, name):
        return cls.functions.get(name)
    
    @classmethod
    def get_functions(cls):
        for function in cls.functions:
            print(function)

        