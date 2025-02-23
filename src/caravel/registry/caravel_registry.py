from typing import Dict, Any, Callable, Optional

class CaravelRegistry:
    functions = {}
    @classmethod
    def register(cls, instance:Optional[object]=None, custom_name=None, is_async=False):
        def decorator(func: Callable):
            name = custom_name or func.__name__
            if instance:
                instance_id = id(instance)
                if instance_id not in cls.functions:
                    cls.functions[instance_id] = {}
                cls.functions[instance_id][name] = [func, is_async]
            else:
                cls.functions[name] = [func, is_async]
            return func    
        return decorator
    
    @classmethod
    def get_function(cls, name, instance: Optional[object]=None):
        if instance:
            instance_id = id(instance)
            return cls.functions.get(instance_id, {}).get(name)
        return cls.functions.get(name)
    
    @classmethod
    def get_functions(cls):
        for key, funcs in cls.functions.items():
            if isinstance(key, int): 
                print(f"Instance {key}: {list(funcs.keys())}")
            else:
                print(f"Global functions: {key}")
    

        