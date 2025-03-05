
template_string NoMarkdown() #"
    Do not use markdown.
"#

template_string NotEnoughContextError(error_message: string, required: string[]) #"
    NotEnoughContextError: {{ error_message }}, required: {{ required }}
"# 

template_string EmptyDictString() #"
    {}
"#

template_string EmptyString() #"
    
"# 

class DynamicJsonObject {
    @@dynamic
} // DynamicJsonObject

enum DynamicJsonEnum {
    @@dynamic
} // DynamicJsonEnum


function GenerateHumanLanguageResponse(json: string, context: string) -> string {
    client "openai/gpt-4o-mini"
    prompt #"

        Describe the content within the following
        {{ json }}
        as if you are answering the prompt in
        {{ context }}
        in a single paragraph. Do not include technical details, just describe the content itself.
        
        {{ ctx.output_format }}
    "#
} // GenerateHumanLanguageResponse

function DynamicGenerateReqBody(context: string) -> DynamicJsonObject {
    client "openai/gpt-4o-mini"
    prompt #"
        Fill out the request body based on the content of the string.
        {{ ctx.output_format }}
    "#

}

enum HTTPMethod {
    GET
    DELETE
    POST
    PATCH
    PUT
}

class APIRequest {
    path string @description(#"
        This is the path that will be attached to the base URL in order to make the API Request.
    "#)
    
    method HTTPMethod @description(#"
        The HTTP method to be employed by the API Request.
    "#)

    params map<string, string> @description(#"
        The query parameters that will be used in the request.
    "#)
    request_body string?
} // APIRequest

// map<string, string> works here because query paramas are ALWAYS strs
function PopulateQueryParameters(fmt: map<string, string | int | float | bool>, context: string) -> map<string, string> {
    client "openai/gpt-4o-mini"
    prompt #"
        DO NOT HALLUCINATE QUERY PARAMS NOT IN {{ fmt }}

        Using the following query parameter structure:
        {{ fmt }}
        And the provided context: {{ context }},
        Complete the query parameters. If the query param structure is empty, return {{ fmt }} with appropriate default values populated.
        {{ ctx.output_format }}
    "#
} // newPopulateQP



test new_function {
    functions [PopulateQueryParameters]
    args {
        fmt {
            "start_cursor" ""
            "filter[acquisition_type][eq]" "loan | lease"
            "filter[reference_number][like]" ""
            "filter[vehicle_id][eq]" ""
            "filter[lender_id][eq]" ""
            "filter[vendor_id][eq]" ""
            "filter[acquisition_date][lt]" ""
            "filter[created_at][lt]" ""
            "filter[updated_at][lt]" ""
            "sort[id]" "desc"
            "sort[acquisition_date]" "asc | desc" 
            "sort[created_at]" "asc | desc"
            "sort[updated_at]" "asc | desc"
        }
        context #"
            Get all of my loan acquisitions from 2010 to 2020 sorted in chronological order.
        "#
    }
}



