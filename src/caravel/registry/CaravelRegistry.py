from typing import Dict, Any, Callable, Optional

class CaravelRegistry:
    functions = {}
    
    @classmethod
    def register(cls, custom_name: Optional[str] = None, is_async:bool = False):
        def decorator(func: Callable):
            def wrapper(instance, *args, **kwargs):
                return func(instance, *args, **kwargs)
            
            wrapper._is_registered = True
            wrapper._custom_name = custom_name or func.__name__
            wrapper._is_async = is_async
            
            return wrapper
        return decorator
    
    @classmethod
    def register_instance(cls, instance):
        instance_id = id(instance)
        if instance_id not in cls.functions:
            cls.functions[instance_id]
        
        for attr_name in dir(instance):
            attr = getattr(instance, attr_name)
            if callable(attr) and hasattr(attr, "_is_registered"):
                name = attr._custom_name
                cls.functions[instance_id][name] = [attr.__get__(instance), attr._is_async]
    
    @classmethod
    def get_function(cls, name, instance: Optional[object] = None):
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

# class CaravelRegistry:
#     functions = {}
#     @classmethod
#     def register(cls, instance:Optional[object]=None, custom_name=None, is_async=False):
#         def decorator(func: Callable):
#             name = custom_name or func.__name__
#             if instance:
#                 instance_id = id(instance)
#                 if instance_id not in cls.functions:
#                     cls.functions[instance_id] = {}
#                 cls.functions[instance_id][name] = [func.__get__(instance), is_async]
#             else:
#                 cls.functions[name] = [func, is_async]
#             return func    
#         return decorator
    
#     @classmethod
#     def get_function(cls, name, instance: Optional[object]=None):
#         if instance:
#             instance_id = id(instance)
#             return cls.functions.get(instance_id, {}).get(name)
#         return cls.functions.get(name)
    
#     @classmethod
#     def get_functions(cls):
#         for key, funcs in cls.functions.items():
#             if isinstance(key, int): 
#                 print(f"Instance {key}: {list(funcs.keys())}")
#             else:
#                 print(f"Global functions: {key}")
    

        