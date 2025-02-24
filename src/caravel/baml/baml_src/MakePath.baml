

template_string NoParamProvided() #"
    NoParamProvidedError
"# // NoParamProbided

function MakePath(path: string, user_input: string) -> string @description(#"
    A string representing the altered path, filled with the path parameters based on the user input.
"#) {
    client "openai/gpt-4o-mini"
    prompt #"
        Using this path outline:
        {{ path }}
        Generate the path with path parameters (if any exist) filled in, using information gleaned from this input:
        {{ user_input }}
        If the parameter cannot be inferred, return:
        {{ NoParamProvided() }}
         If no path parameter exists within {{ path }}, return:
        {{ path }}
        {{ ctx.output_format }}
    "#
} // MakePath

test make_path_param_given {
    functions [MakePath]
    args {
        path #"/v1/vehicles/{id}"#
        user_input #"Get vehicle with id 1234"#
    }
}

test make_path_param_not_given {
    functions [MakePath]
    args {
        path #"/v1/vehicles/{id}"#
        user_input #"Can you get my dad's truck from fleetio? "#
    }
}

test make_path_no_path_param_present {
    functions [MakePath]
    args {
        path #"/v1/vehicles/"#
        user_input #"Can you give me all of my vehicles in fleetio?"#
    }
}