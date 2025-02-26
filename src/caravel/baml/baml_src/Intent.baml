function GetIntent(intents: string[], intent: string) -> string @description(#"
    A string formatted in the following manner: <METHOD Intent>, where METHOD is the HTTP Request that will need to be used. 
"#) {
    client "openai/gpt-4o-mini"
    prompt #"
        Using the following list of intents, 
        {{ intents }}
        and the user-prompted intent:
        {{ intent }}
        output the intent, sans quotes.
        {{ ctx.output_format }}   
    "#
} // GetIntent


function MapContextToParams(context: string) -> map<string, string> {
    client "openai/gpt-4o-mini"
    prompt #"
        Parametrize the context:
        {{ context }}
        Such that a mapping is created between the parameters given in the context and their values.

        {{ ctx.output_format }}
    "#
}

test map_ctx {
    functions [MapContextToParams]
    args {
        context "I want to add a new vehicle to fleetio. The name is cannons truck, the vehicles type id is 10, the unit metrics are miles, and the status id is 20. "
    }
}

test get_intent {
    functions [GetIntent]
    args {
        intents [
            "POST Add a new vehicle to Fleetio",
            "GET Get a vehicle from Fleetio",
            "PATCH Edit a vehicle in Fleetio" 
        ]
        intent #"upload a new vehicle to fleetio"#
    } // args
} // get_intent