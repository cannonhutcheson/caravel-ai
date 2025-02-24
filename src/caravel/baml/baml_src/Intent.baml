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