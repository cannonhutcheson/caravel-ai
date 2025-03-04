

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


class DynamicAPIRequest {
    path string
    method HTTPMethod
    params  map<string, string>?
    request_body DynamicObject?
} // DynamicAPIRequest

function ConstructDynamicAPIRequest(path: string, method: HTTPMethod | string, params: map<string, string>?, request_body: DynamicObject?) -> DynamicAPIRequest {
    client "openai/gpt-4o-mini"
    prompt #"
        Using
        {{ path }}
        {{ method }}
        {{ params }}
        {{ request_body }}
        {{ ctx.output_format }}
    "#
} // ConstructDynamicAPIRequest

test api_req_dyn {
    functions [ConstructDynamicAPIRequest]
    args {
        path "/addresses"
        method GET
    } // args
}