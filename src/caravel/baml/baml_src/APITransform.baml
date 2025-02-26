
///
class RequestBody {
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
} // RequestBody

function ExtractRequestBodySchema(req_body_json: string) -> RequestBody {
  client "openai/gpt-4o-mini"
  prompt #"
    Extract from this content:
    {{ req_body_json }}
    {{ ctx.output_format }}
  "#
} // ExtractRequestBody

class APIRequestFormer {
  params map<string, string> @description(#"
    A mapping of the parameters to their associated values based on user input. Should contain all required values (empty if not given). Do not include nonpopulated, nonrequired values.
  "#)
} // APIRequest

function CreateAPIRequestBody(schema: RequestBody, user_prompt: string) -> APIRequest {
  client "openai/gpt-4o-mini"
  prompt ###"
    Using the following schema:
    {{ schema }}
    To analyze the user prompt:
    {{ user_prompt }}
    {{ctx.output_format}}
  "###
} // MakeRequestBody

test api_request_construction {
  functions [CreateAPIRequestBody]
  args {
    user_prompt #"
      Make a new service entry for vehicle (id 2), completed today. 
    "#
    schema {
      endpoint "/v2/service_entries"
      required ["completed_at", "vehicle_id", "meter_entry_attributes"]
      required_types ["string", "string", "object"]
      all_params [
        "completed_at", 
        "started_at", 
        "vehicle_id", 
        "vehicle_vin", 
        "vendor_id", 
        "reference", 
        "label_list", 
        "general_notes", 
        "vmrs_repair_priority_class_id", 
        "custom_fields", 
        "meter_entry_attributes", 
        "secondary_meter_entry_attributes", 
        "service_entry_line_items_attributes", 
        "issue_ids", 
        "service_task_ids", 
        "comments_attributes", 
        "documents_attributes", 
        "images_attributes", 
        "labor_subtotal", 
        "parts_subtotal", 
        "subtotal", 
        "discount", 
        "discount_percentage", 
        "discount_type", 
        "tax_1", 
        "tax_1_percentage", 
        "tax_1_type", 
        "tax_2", 
        "tax_2_percentage", 
        "tax_2_type", 
        "total_amount", 
      ]
      all_types [
        "string", 
        "string", 
        "object", 
        "string", 
        "string", 
        "string", 
        "object", 
        "string", 
        "string", 
        "object", 
        "array", 
        "array", 
        "array", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
        "number", 
      ]
    }
}
} // api_request_construction

test api_req_body {
  functions [ExtractRequestBodySchema]
  args {
    req_body_json ###"
     "/v2/service_entries": {
            "description": "Creates a new Service Entry",
            "request_body_example": {
                "completed_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2023-03-14T13:46:27-06:00",
                    "description": "The date and time at which the Service Entry was completed.\nWe recommend using [ISO-8601](/docs/overview/date-formatting)\nformatted dates to avoid ambiguity."
                },
                "started_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2023-03-14T13:46:27-06:00",
                    "description": "The date and time at which the Service Entry was started.\nWe recommend using [ISO-8601](/docs/overview/date-formatting)\nformatted dates to avoid ambiguity."
                },
                "vehicle_id": {
                    "$ref": "#/components/schemas/Id"
                },
                "vehicle_vin": {
                    "type": "string",
                    "maxLength": 17,
                    "description": "The VIN of the `Vehicle` associated with this Service Entry."
                },
                "vendor_id": {
                    "$ref": "#/components/schemas/Id"
                },
                "reference": {
                    "type": "string",
                    "maxLength": 255,
                    "description": "A reference number for this Service Entry."
                },
                "label_list": {
                    "$ref": "#/components/schemas/LabelListParameters"
                },
                "general_notes": {
                    "type": "string",
                    "description": "Any general notes about this Service Entry."
                },
                "vmrs_repair_priority_class_id": {
                    "$ref": "#/components/schemas/Id"
                },
                "custom_fields": {
                    "$ref": "#/components/schemas/CustomFields"
                },
                "meter_entry_attributes": {
                    "description": "A Service Entry may be associated with a [Meter\nEntry](/docs/api/meter-entries)",
                    "type": "object",
                    "properties": {
                        "value": {
                            "type": "number",
                            "format": "float",
                            "example": "108043",
                            "description": "The value is the actual number on the meter that increments over time.  The unit is determined by the [configured `meter_unit`](https://help.fleetio.com/s/article/Fuel-Settings#vehicle-settings) on the associated Vehicle."
                        },
                        "void": {
                            "type": "boolean",
                            "description": "If you attempt to save a meter value, which is too high or too low, Fleetio's validation rules will reject it. If you need to bypass this validation, you may [mark an entry as void](https://help.fleetio.com/s/article/Meter-Entry-Mark-As-Void-Unmark-As-Void)."
                        }
                    }
                },
                "secondary_meter_entry_attributes": {
                    "description": "A Service Entry may also be associated with a secondary [Meter\nEntry](/docs/api/meter-entries)",
                    "type": "object",
                    "properties": {
                        "value": {
                            "type": "number",
                            "format": "float",
                            "example": "108043",
                            "description": "The value is the actual number on the meter that increments over time.  The unit is determined by the [configured `meter_unit`](https://help.fleetio.com/s/article/Fuel-Settings#vehicle-settings) on the associated Vehicle."
                        },
                        "void": {
                            "type": "boolean",
                            "description": "If you attempt to save a meter value, which is too high or too low, Fleetio's validation rules will reject it. If you need to bypass this validation, you may [mark an entry as void](https://help.fleetio.com/s/article/Meter-Entry-Mark-As-Void-Unmark-As-Void)."
                        }
                    }
                },
                "service_entry_line_items_attributes": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/ServiceEntryLineItemAttributes"
                    }
                },
                "issue_ids": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/Id"
                    },
                    "description": "The IDs of any Issues associated with this Service Entry."
                },
                "service_task_ids": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/Id"
                    },
                    "description": "The IDs of any Service Tasks associated with this Service Entry."
                },
                "comments_attributes": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/CommentsAttributes"
                    }
                },
                "documents_attributes": {
                    "type": "array",
                    "description": "An array of one or more document objects to add to the record.\nFollow our [Attaching Documents and Images](/docs/overview/attaching-documents-and-images) guide\nto upload to our third party storage provider in order to obtain `file_url`.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The name to give the file which will be shown in the UI."
                            },
                            "file_url": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The URL obtained from our storage provider that points to the file."
                            },
                            "file_mime_type": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The MIME type of the file. For example, `application/pdf`."
                            },
                            "file_name": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The name of the file."
                            },
                            "file_size": {
                                "type": "integer",
                                "description": "The size of the file in bytes."
                            }
                        }
                    }
                },
                "images_attributes": {
                    "type": "array",
                    "description": "An array of one or more image objects to add to the record.\nFollow our [Attaching Documents and Images](/docs/overview/attaching-documents-and-images) guide\nto upload to our third party storage provider in order to obtain `file_url`.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The name to give the image which will be shown in the UI."
                            },
                            "file_url": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The URL obtained from our storage provider that points to the image."
                            },
                            "file_mime_type": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The MIME type of the image. For example, `image/png`."
                            },
                            "file_name": {
                                "type": "string",
                                "maxLength": 255,
                                "description": "The name of the image."
                            },
                            "file_size": {
                                "type": "integer",
                                "description": "The size of the image file in bytes."
                            }
                        }
                    }
                },
                "labor_subtotal": {
                    "type": "number",
                    "format": "float",
                    "description": "The total cost of labor for this Service Entry.\nThis is calculated by summing the `labor_cost` of each `Service Entry Line Item`."
                },
                "parts_subtotal": {
                    "type": "number",
                    "format": "float",
                    "description": "The total cost of `Parts` for this Service Entry.\nThis is calculated by summing the `parts_cost` of each `Service Entry Line Item`."
                },
                "subtotal": {
                    "type": "number",
                    "format": "float",
                    "description": "The subtotal amount of this Service Entry before any discounts or taxes.\nThis is calculated by summing the `subtotal` of each `Service Entry Line Item`."
                },
                "discount": {
                    "type": "number",
                    "format": "float",
                    "description": "The total discount amount for this Service Entry."
                },
                "discount_percentage": {
                    "type": "number",
                    "format": "float",
                    "description": "The total discount percentage for this Service Entry."
                },
                "discount_type": {
                    "$ref": "#/components/schemas/DiscountType"
                },
                "tax_1": {
                    "type": "number",
                    "format": "float",
                    "description": "The first tax amount for this Service Entry."
                },
                "tax_1_percentage": {
                    "type": "number",
                    "format": "float",
                    "description": "The first tax percentage for this Service Entry."
                },
                "tax_1_type": {
                    "$ref": "#/components/schemas/TaxType"
                },
                "tax_2": {
                    "type": "number",
                    "format": "float",
                    "description": "The second tax amount for this Service Entry."
                },
                "tax_2_percentage": {
                    "type": "number",
                    "format": "float",
                    "description": "The second tax percentage for this Service Entry."
                },
                "tax_2_type": {
                    "$ref": "#/components/schemas/TaxType"
                },
                "total_amount": {
                    "type": "number",
                    "format": "float",
                    "description": "The grand total of this Service Entry."
                }
            },
            "required": [
                "completed_at",
                "vehicle_id",
                "meter_entry_attributes"
            ]
        },
    
    "###
  }
}


///