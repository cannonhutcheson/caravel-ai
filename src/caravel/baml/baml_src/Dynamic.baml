

// A dynamic class that will be used for checking the schema of OpenAPI specifications
class DynamicObject {
    @@dynamic
} // DynamicObject

// A dynamic enum that will be used for constructing dynamic json objects.
enum DynamicEnum {
    @@dynamic
} // DynamicEnum

function ExtractDynamicTypes(context: string) -> DynamicObject{
    client "openai/gpt-4o-mini"
    prompt #"
        {{ ctx.output_format }}
        {{ _.role('user') }}
        Extract from this content:
        {{ context }}
    "#
} // ExtractDynamicTypes

