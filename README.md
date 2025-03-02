## caravel-ai README
Caravel makes it easy to develop AI Agents that interact with third-party APIs. Caravel AI is open source and free to use.


## Installation
```bash
installation cmd goes here
```

# Overview
Caravel projects have four main parts:
1. The Parser
The Parser is a class that provides utilities for operating on OpenAPI specification files. The Parser is used to convert the OpenAPI specifications into formats that make it workable with the Client and the Runner.
2. The Runner 
The Runner is a class consisting of methods that perform legwork such as constructing API requests, checking the schema of requests, etc.
3. The Client
The Client is a class that is used to make HTTP requests to the API. Client functions recieve their parameters from the runner and return their results in JSON format or in human/LLM-readable text. In addition to the standard HTTP methods, the Client also allows users to add their own custom methods to the client.
4. The CaravelRegistry
The CaravelRegistry is a function registry class. This registry is what allows developers to call Caravel functions from their assistant. The CaravelRegistry is a singleton class.
