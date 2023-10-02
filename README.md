# Memento

Memento is a framework for building AI agents that can complete complex tasks by combining simple modular skills. The goal is to create assistants that understand natural language, break down requests, and leverage existing tools to satisfy user needs.

## Background

The name Memento comes from the Christopher Nolan movie [Memento](https://en.wikipedia.org/wiki/Memento_(film)), where the main character uses notes to self in order to overcome his short-term memory loss. This only works because he breaks down his goals into smaller tasks that can be completed with the help of his notes, and then updates the notes as he goes along.

 This software (Memento) uses a similar technique to create AI agents that can complete complex tasks by combining simple modular skills. The goal is to create assistants that understand natural language, break down requests, and leverage existing tools to satisfy user needs.

## Key Ideas

Memento is built around a few core principles:

- **Composability:** Complex behaviors are built by combining simple, single-purpose skills called "tools".
- **Language-centric:** All interaction is through natural language messages.
- **Tool abstraction:** Tools can be anything from scripts to ML models, as long as they use the messaging protocol.
- **Scalable reasoning:** Language models compose behaviors and handle planning, even as skills grow.

## Architecture

At runtime, a Memento agent consists of:

- A language model (like GPT-3.5, GPT-4 or Anthropic Claude) for conversation and reasoning.
- A tools manager that invokes available tools.
- A prompts manager that provides prompt templates.

Here is how they work together:

1. The agent receives a user's natural language request.
2. The request is formatted with the agent prompt and sent to the language model.
3. The model outputs a tool invocation message.
4. The tools manager runs the tool and captures the result. 
5. The agent evaluates the output and decides which tool to call next. (Calling the user tool can be used to ask for aditional information or to provide a final response.)
6 Steps 3-5 repeat until the agent is satisfied the task is complete.


## Adding Skills 

New behaviors are added by creating focused tools. Two types of tools can be created: 

- **Subprocess tools** are simple scripts or programs that provide a single skill. They connect to the agent via a simple messaging protocol.
- **Subordinate agents** are Memento agents that have their own prompt. They are run in the same process as the main agent and managed by the same class as the top-level agent. 
 
The protocol between agent and tools is defined in the toolsmith prompt. It is a simple text-based protocol that enable the agent to send and receive messages.

For example a hypothetical calendar tool can be accessed by the agent like this :
```
{{FROM:agent TO:calendar}}
list_meetings 
{{END}}

{{FROM:calendar TO:agent}}  
Team meeting 10am Monday
1-on-1 2pm Wednesday
{{END}} 
```

Subprocess tools implement a protocol that uses stdin/stdout to get requests and provide responses to the agent. 

## Usage

See the `bots` directory for examples, like a text adventure game, email client, and code interaction bot.

To run an agent:

- Install dependencies (pip install -r requirements.txt)
- Change to a bot directory 
- Run `python memento.py --model <model_id>`

Use `--help` for a list of available models.
