
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

class RequestDataStorage {
  required string[] @description(#"
    The list of required parameters. It will appear in an array at the end of JSON.
  "#)
  required_types string[] @description(#"
    A list of JSON types, reflecting the types of the required parameters.
  "#)
  all_params string[] @description(#"
    A list of all the allowed parameters, including those required.
  "#)
  all_types string[] @description(#"
    A list of JSON types, reflecting the types of all allowed parameters.
  "#)
} // ReqBody

class APIRequest {
    path string @description(#"
        This is the path that will be attached to the base URL in order to make the API Request.
    "#)
    params string @description(#"
        This will be the query parameters of the path. 
    "#)
    request_body string
} // APIRequest

function ExtractReqBodyFormat(req_body_json: string, required_req: string[]) -> RequestDataStorage {
    client "openai/gpt-4o-mini"
    prompt #"
        Extract from this content:
        {{ req_body_json }}
        {{ required_req }}
        {{ ctx.output_format }}
    "#
} // ExtractReqBodyFormat

function PopulateRequestBody(req_body_format: RequestDataStorage, context: string) -> string @description(#"
    A stringified JSON object that could be passed to the HTTPX Client object in the `json` argument once parsed. It should begin and end with brackets.
"#) {
    client "openai/gpt-4o-mini"
    prompt #"

        {{ NoMarkdown() }}

        Populate the request body given the following information:
        {{ req_body_format }}
        {{ context }}
        If {{ req_body_format }} is empty return {{ EmptyString() }}
        If not enough context is provided to fill all required fields, return:
        {{ NotEnoughContextError("There is insufficient information to make the API Request Body. Prompt the user for the missing info: ", req_body_format.required) }}
        {{ ctx.output_format }}
    "#
} // PopulateRequestBody

function PopulateQueryParameters(fmt: map<string, string>, context: string) -> map<string, string> {
    client "openai/gpt-4o-mini"
    prompt #"
        Using the following query parameter structure:
        {{ fmt }}
        And the provided context: {{ context }},
        Complete the query parameters.
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

test populate_request_body {
    functions [PopulateRequestBody]
    args {
        req_body_format {
            required [
                "name",
                "primary_meter_unit",
                "vehicle_status_id",
                "vehicle_type_id",
            ]
            required_types [
                "string",
                "object",
                "integer",
                "integer",
            ]
            all_params [
                "color",
                "fuel_type_id",
                "fuel_volume_units",
                "group_id",
                "group_hierarchy",
                "label_ids",
                "license_plate",
                "make",
                "primary_meter_unit",
                "model",
                "name",
                "ownership",
                "registration_expiration_month",
                "registration_state",
                "secondary_meter",
                "secondary_meter_unit",
                "system_of_measurement",
                "trim",
                "vehicle_status_id",
                "vehicle_type_id",
                "vin",
                "year",
                "linked_vehicle_ids",
                "purchase_detail",
                "external_ids",
                "vehicle_status_name",
                "vehicle_type_name",
                "in_service_date",
                "in_service_meter_value",
                "estimated_service_months",
                "estimated_replacement_mileage",
                "estimated_resale_price",
                "out_of_service_date",
                "out_of_service_meter_value",
                "specs",
                "custom_fields",
            ]
            all_types [
                "object",
                "integer",
                "integer",
                "integer",
                "string",
                "array",
                "string",
                "string",
                "object",
                "string",
                "string",
                "object",
                "integer",
                "string",
                "boolean",
                "object",
                "object",
                "string",
                "integer",
                "string",
                "string",
                "array",
                "object",
                "string",
                "string",
                "string",
                "string",
                "integer",
                "string",
                "string",
                "string",
                "object",
                "object",
                "string",
                "string",
                "number",
                "number",
                "number",
                "number",
                "string",
                "string",
                "boolean",
                "number",
                "number",
                "string",
                "string",
                "string",
                "string",
                "number",
                "number",
                "number",
                "number",
                "object",
                "object",
                "object",
                "object",
            ]
        }
        context #"I want to post a new vehicle to fleetio. the name is cannons truck,  meter units are in miles, the status id is 10, and the type id is 20"#
    }
}


test populate_request_body_param_missing {
    functions [PopulateRequestBody]
    args {
        req_body_format {
            required [
                "name",
                "primary_meter_unit",
                "vehicle_status_id",
                "vehicle_type_id",
            ]
            required_types [
                "string",
                "object",
                "integer",
                "integer",
            ]
            all_params [
                "color",
                "fuel_type_id",
                "fuel_volume_units",
                "group_id",
                "group_hierarchy",
                "label_ids",
                "license_plate",
                "make",
                "primary_meter_unit",
                "model",
                "name",
                "ownership",
                "registration_expiration_month",
                "registration_state",
                "secondary_meter",
                "secondary_meter_unit",
                "system_of_measurement",
                "trim",
                "vehicle_status_id",
                "vehicle_type_id",
                "vin",
                "year",
                "linked_vehicle_ids",
                "purchase_detail",
                "external_ids",
                "vehicle_status_name",
                "vehicle_type_name",
                "in_service_date",
                "in_service_meter_value",
                "estimated_service_months",
                "estimated_replacement_mileage",
                "estimated_resale_price",
                "out_of_service_date",
                "out_of_service_meter_value",
                "specs",
                "custom_fields",
            ]
            all_types [
                "object",
                "integer",
                "integer",
                "integer",
                "string",
                "array",
                "string",
                "string",
                "object",
                "string",
                "string",
                "object",
                "integer",
                "string",
                "boolean",
                "object",
                "object",
                "string",
                "integer",
                "string",
                "string",
                "array",
                "object",
                "string",
                "string",
                "string",
                "string",
                "integer",
                "string",
                "string",
                "string",
                "object",
                "object",
                "string",
                "string",
                "number",
                "number",
                "number",
                "number",
                "string",
                "string",
                "boolean",
                "number",
                "number",
                "string",
                "string",
                "string",
                "string",
                "number",
                "number",
                "number",
                "number",
                "object",
                "object",
                "object",
                "object",
            ]
        }
        context #"I want to post a new vehicle to fleetio.  meter units are in miles, the status id is 10, and the type id is 20"#
    }
}


function ConstructAPIRequest(path: string, params: string, request_body: string) -> APIRequest {
    client "openai/gpt-4o-mini"
    prompt #"
        Using 
        {{ path }}
        {{ params }}
        {{ request_body }}
        Output
        {{ ctx.output_format }}
    "#
} // ConstructAPIRequest

function ExtractQueryParamsFormat(params: string[], required: string[]) -> RequestDataStorage {
    client "openai/gpt-4o-mini"
    prompt #"
        Extract from this content:
        {{ params }}
        {{ required }}
        {{ ctx.output_format }}
    "#
} // ExtractQueryParamsFormat

