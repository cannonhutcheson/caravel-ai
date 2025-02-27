
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

function DynamicGenerateReqBody(context: string) -> DynamicJsonObject {
    client "openai/gpt-4o-mini"
    prompt #"
        Fill out the request body based on the content of the string.
        {{ ctx.output_format }}
    "#

}

function PopulateRequestBody(fmt: string, required: string[], context: string, date: string) -> string {
    client "openai/gpt-4o-mini"
    prompt #"

        {{ NoMarkdown() }}
        Always use double quotes when quotes are needed. The first and last char should be { and } respectively. Sometimes, arrays of boolean values will be given. Rather than returning an uppercase boolean value in an array, return a lowercase boolean value, not in an array. Sometimes, date fields are given, listed as strings. Give a date in ISO format based on {{ date }}
        Given the format of a request body in string format:
        {{ fmt }}
        The required fields in the request body:
        {{ required }}
        And the given context: {{ context }}
        Fill in the request body, ensuring all required fields are returned. Do not include fields that are both unrequired and unfilled. 
        {{ ctx.output_format }}
    "#
} // NewPopulateRB


test new_pop_rb {
    functions [PopulateRequestBody]
    args {
        fmt #"
            {'color': '<string>', 'fuel_type_id': 0, 'fuel_volume_units': 'us_gallons | uk_gallons | liters', 'group_id': 0, 'group_hierarchy': '<string>', 'label_ids': ['<array>'], 'license_plate': '<string>', 'make': '<string>', 'primary_meter_unit': 'km | hr | mi', 'model': '<string>', 'name': '<string>', 'ownership': 'owned | leased | rented | customer', 'registration_expiration_month': 0, 'registration_state': '<string>', 'secondary_meter': [True, False], 'secondary_meter_unit': 'km | hr | mi', 'system_of_measurement': 'imperial | metric', 'trim': '<string>', 'vehicle_status_id': 0, 'vehicle_type_id': 0, 'vin': '<string>', 'year': 0, 'linked_vehicle_ids': ['<array>'], 'purchase_detail': {'comment': '<string>', 'date': '<string>', 'price': 0.0, 'vendor_id': 0, 'warranty_expiration_date': '<string>', 'warranty_expiration_meter_value': 0.0, 'meter_entry_attributes.value': 0.0, 'meter_entry_attributes.void': [True, False]}, 'external_ids': {}, 'vehicle_status_name': '<string>', 'vehicle_type_name': '<string>', 'in_service_date': '<string>', 'in_service_meter_value': '<string>', 'estimated_service_months': 0, 'estimated_replacement_mileage': 0.0, 'estimated_resale_price': 0.0, 'out_of_service_date': '<string>', 'out_of_service_meter_value': '<string>', 'specs': {'base_towing_capacity': 0.0, 'bed_length': 0.0, 'body_subtype': '<string>', 'body_type': '<string>', 'brake_system': '<string>', 'cargo_volume': 0.0, 'curb_weight': 0.0, 'drive_type': '<string>', 'engine_aspiration': '<string>', 'engine_block_type': '<string>', 'engine_bore': 0.0, 'engine_brand': '<string>', 'engine_cam_type': '<string>', 'engine_compression': 0.0, 'engine_cylinders': 0, 'engine_description': '<string>', 'engine_displacement': 0.0, 'engine_stroke': 0.0, 'engine_valves': 0, 'epa_city': 0.0, 'epa_combined': 0.0, 'epa_highway': 0.0, 'front_tire_psi': 0.0, 'front_tire_type': '<string>', 'front_track_width': 0.0, 'front_wheel_diameter': '<string>', 'fuel_induction': '<string>', 'fuel_quality': '<string>', 'fuel_tank_capacity': 0.0, 'fuel_tank_2_capacity': 0.0, 'gross_vehicle_weight_rating': 0.0, 'ground_clearance': 0.0, 'height': 0.0, 'interior_volume': 0.0, 'length': 0.0, 'max_hp': 0, 'max_payload': 0.0, 'max_torque': 0, 'msrp': 0.0, 'oil_capacity': 0.0, 'passenger_volume': '<string>', 'rear_axle_type': '<string>', 'rear_tire_psi': 0.0, 'rear_tire_type': '<string>', 'rear_track_width': 0.0, 'rear_wheel_diameter': '<string>', 'redline_rpm': '<string>', 'transmission_brand': '<string>', 'transmission_description': '<string>', 'transmission_gears': 0, 'transmission_type': '<string>', 'wheelbase': 0.0, 'width': 0.0}, 'custom_fields': {}}
        "#
        required [
            "name"
            "primary_meter_unit"
            "vehicle_status_id"
            "vehicle_type_id"
            ]
        context "I want to create a new vehicle in fleetio. name it cannons truck, give it a status id of 1, a type id of 2, and a primary meter unit in miles"
        date "2/27/2025"
    } // args
} // new_pop_rb


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

