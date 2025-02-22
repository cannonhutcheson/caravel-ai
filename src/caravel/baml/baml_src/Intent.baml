function GetIntent(intents: string[], intent: string) -> string {
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