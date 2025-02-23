import pytest
from src.caravel.registry.CaravelRegistry import CaravelRegistry

# Sample functions to register
def sample_func():
    return "Hello, Caravel!"

async def async_func():
    return "Hello, Async Caravel!"

class SampleClass:
    def method(self):
        return "Instance Method"

# Test registering a global function
def test_register_global_function():
    CaravelRegistry.register()(sample_func)
    registered_func = CaravelRegistry.get_function("sample_func")
    assert registered_func is not None
    assert registered_func[0]() == "Hello, Caravel!"
    assert registered_func[1] is False  # Not async

# Test registering an instance function (Fixed)
def test_register_instance_function():
    instance = SampleClass()
    CaravelRegistry.register(instance=instance)(instance.method)
    
    registered_func = CaravelRegistry.get_function("method", instance)
    assert registered_func is not None
    
    # Call directly without needing __get__()
    assert registered_func[0]() == "Instance Method"

# Test registering an async function
def test_register_async_function():
    CaravelRegistry.register(custom_name="async_test", is_async=True)(async_func)
    registered_func = CaravelRegistry.get_function("async_test")
    assert registered_func is not None
    assert registered_func[0] == async_func
    assert registered_func[1] is True  # Should be async

# Test retrieving a non-existent function
def test_get_non_existent_function():
    assert CaravelRegistry.get_function("does_not_exist") is None

# Test retrieving all functions (captures printed output)
def test_get_functions(capfd):
    CaravelRegistry.get_functions()
    captured = capfd.readouterr()
    assert "Global functions:" in captured.out or "Instance" in captured.out
