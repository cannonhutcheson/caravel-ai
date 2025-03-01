from typing import Any, Dict
from src.caravel.baml.baml_client.type_builder import TypeBuilder, FieldType

from pydantic import BaseModel

class SchemaAdder:
    def __init__(self, tb: TypeBuilder, schema: Dict[str, Any], spec: dict):
        self.tb = tb
        self.schema = schema
        self._ref_cache = {}
        self.spec = spec
        self.existing_classes = set()

    # def _parse_object(self, json_schema: Dict[str, Any]) -> FieldType:
    #     assert json_schema["type"] == "object"
    #     name = json_schema.get("title")
    #     if name is None:
    #         raise ValueError("Title is required in JSON schema for object type")

    #     required_fields = json_schema.get("required", [])
    #     assert isinstance(required_fields, list)

    #     new_cls = self.tb.add_class(name)
    #     if properties := json_schema.get("properties"):
    #         assert isinstance(properties, dict)
    #         for field_name, field_schema in properties.items():
    #             assert isinstance(field_schema, dict)
    #             default_value = field_schema.get("default")
    #             field_type = self.parse(field_schema)
    #             if field_name not in required_fields:
    #                 if default_value is None:
    #                     field_type = field_type.optional()
    #             property = new_cls.add_property(field_name, field_type)
    #             if description := field_schema.get("description"):
    #                 assert isinstance(description, str)
    #                 if default_value is not None:
    #                     description = (
    #                         description.strip() + "\n" + f"Default: {default_value}"
    #                     )
    #                     description = description.strip()
    #                 if len(description) > 0:
    #                     property.description(description)
    #     return new_cls.type()

    # 
    
    # def _parse_object(self, json_schema: Dict[str, Any], parent_key: str = None) -> FieldType:
    #     """
    #     Parses an object schema, using parent_key as the title if no title is provided.
    #     """
    #     # assert json_schema["type"] == "object"

    #     # Use parent_key if the object does not have a title
    #     name = json_schema.get("title", parent_key)
    #     if name is None:
    #         raise ValueError("Title is required in JSON schema for object type")

    #     required_fields = json_schema.get("required", [])
    #     assert isinstance(required_fields, list)

    #     # Create a new class with the resolved name
    #     new_cls = self.tb.add_class(name)

    #     if properties := json_schema.get("properties"):
    #         assert isinstance(properties, dict)

    #         for field_name, field_schema in properties.items():
    #             assert isinstance(field_schema, dict)

    #             # Pass the field name as the new parent key
    #             field_type = self.parse(field_schema, parent_key=field_name)

    #             if field_name not in required_fields:
    #                 field_type = field_type.optional()

    #             new_cls.add_property(field_name, field_type)

    #     return new_cls.type()

    def _parse_object(self, json_schema: Dict[str, Any], parent_key: str) -> FieldType:
        """Parses an object type from JSON schema, using the parent key to name the class."""

        # assert json_schema["type"] == "object"

        # ✅ Ensure the object gets a meaningful name based on parent_key
        if not parent_key:
            raise ValueError("parent_key is required to name the object correctly.")

        print(f"Parsing object: {parent_key}")  # Debugging output

        required_fields = json_schema.get("required", [])
        assert isinstance(required_fields, list)

        # ✅ If this class has already been created, return its type
        if parent_key in self.existing_classes:
            print(f"Skipping duplicate class definition for {parent_key}")
            return self.tb.get_class(parent_key).type()

        # ✅ Create a new class with the provided parent_key
        self.existing_classes.add(parent_key)
        new_cls = self.tb.add_class(parent_key)
    
        if properties := json_schema.get("properties"):
            assert isinstance(properties, dict)

            for field_name, field_schema in properties.items():
                assert isinstance(field_schema, dict)

                default_value = field_schema.get("default")

                # ✅ Recursively call parse, using the field name as the new parent_key
                field_type = self.parse(field_schema, parent_key=field_name)

                if field_name not in required_fields:
                    if default_value is None:
                        field_type = field_type.optional()

                property = new_cls.add_property(field_name, field_type)

                if description := field_schema.get("description"):
                    assert isinstance(description, str)
                    if default_value is not None:
                        description = (
                            description.strip() + "\n" + f"Default: {default_value}"
                        )
                        description = description.strip()
                    if len(description) > 0:
                        property.description(description)

        return new_cls.type()


    def _parse_string(self, json_schema: Dict[str, Any]) -> FieldType:
        assert json_schema["type"] == "string"
        title = json_schema.get("title")

        if enum := json_schema.get("enum"):
            assert isinstance(enum, list)
            if title is None:
                # Treat as a union of literals
                return self.tb.union([self.tb.literal_string(value) for value in enum])
            new_enum = self.tb.add_enum(title)
            for value in enum:
                new_enum.add_value(value)
            return new_enum.type()
        return self.tb.string()

    def _load_ref(self, ref_path: str) -> FieldType:
        keys = ref_path.lstrip("#/").split("/")
        schema = self.spec
        
        for key in keys:
            schema = schema.get(key, {})
            
        if "$ref" in schema:
            return self._load_ref(schema["$ref"])
        
        # return self.parse(schema, parent_key=keys[-1])
        return schema
    
   
   
    def parse(self, json_schema: Dict[str, Any], parent_key:str=None) -> FieldType:
        if any_of := json_schema.get("anyOf"):
            assert isinstance(any_of, list)
            return self.tb.union([self.parse(sub_schema) for sub_schema in any_of])

        if ref := json_schema.get("$ref"):
            assert isinstance(ref, str)
            # return self._load_ref(ref)
            resolved_ref = self._load_ref(ref)
            ref_name = ref.split("/")[-1]
            return self.parse(resolved_ref, parent_key=ref_name)
            
        
        type_ = json_schema.get("type")
        if type_ is None:
            raise ValueError(f"Type is required in JSON schema: {json_schema}")
        parse_type = {
            "string": lambda: self._parse_string(json_schema),
            "number": lambda: self.tb.float(),
            "integer": lambda: self.tb.int(),
            "object": lambda: self._parse_object(json_schema, parent_key),
            "array": lambda: self.parse(json_schema["items"], parent_key).list() if "items" in json_schema else self.tb.list_of(self.tb.any()),
            "boolean": lambda: self.tb.bool(),
            "null": lambda: self.tb.null(),
        }

        if type_ not in parse_type:
            raise ValueError(f"Unsupported type: {type_}")

        field_type = parse_type[type_]()
        print(field_type)
        return field_type


def parse_json_schema(json_schema: Dict[str, Any], tb: TypeBuilder, spec: dict) -> FieldType:
    parser = SchemaAdder(tb, json_schema, spec)
    return parser.parse(json_schema, parent_key="root")