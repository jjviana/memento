# Memento

Memento is a framework that enables the creation of AI agents that can autonomously discover and use tools to fulfill complex user requests. Far from being a production-ready system, it is a research tool for investigating the possibilities and limitations os the current generation of Large Language Models for planning, reasoning, and comprehension. 

## Background

The name Memento comes from the Christopher Nolan movie [Memento](https://en.wikipedia.org/wiki/Memento_(film)), where the main character uses notes to self in order to overcome his short-term memory loss. This only works because he breaks down his goals into smaller tasks that can be completed with the help of his notes, and then updates the notes as he goes along.

Memento (the software) uses a similar technique to create AI agents that can complete complex tasks by combining simple modular skills. At each step, the agent evaluates the request and the outputs of the previous steps and decides on the next step. By repeatedly doing that agents can accomplish fairly complex tasks even in the absence of long-term memory. 

## Key Ideas

Memento is built around a few core principles:

- **Composability:** Complex behaviors are built by combining simple, single-purpose skills called "tools".
- **Language-centric:** All interaction is through natural language messages.
- **Tool abstraction:** Tools can be anything from scripts to ML models, as long as they implement the tool  messaging protocol.
- **Scalable reasoning:** Language models compose behaviors and handle planning, even as skills grow. Complex tasks can be delegated to traditional software or to specialized agents. These sub-agents can in turn discover and use their own tools. 

## Architecture

At runtime, a Memento agent consists of:

- A language model (like GPT-3.5, GPT-4, or Anthropic Claude) for conversation and reasoning.
- A tools manager that invokes available tools.
- A prompts manager that provides prompt templates.

Here is how they work together:

1. The agent receives a user's natural language request.
2. The request is formatted with the agent prompt and sent to the language model.
3. The model outputs a tool invocation message.
4. The tools manager runs the tool and captures the result.
5. The result is sent to the language model, together with the past interaction history.
6. The language model evaluates the output and decides which tool to call next. Calling the user tool can be used to ask for additional information or to provide a final response.)
7 Steps 3-6 are repeated until the agent is satisfied that the task is complete.

## The prompt

The initial prompt to the language model lays out the protocol for communication with tools. The protocol is based on message passing, with the agent being able to send and receive messages to or from tools. The general format of the protocol messages is:
```
{{FROM:entityId1 TO:entityId2}}
content
{{END}}
```
The agent itself is identified by the entity id 'memento'. All the other entities are tools, and there are two special tools:

- *user*: enables the agent to send and receive messages from the user
- *system*: enables the agent to send and receive messages to the system.

The system tool implements a simple directory of tools, that the agent can discover by sending the *list_tools* command. This provides the agent with an initial list of tools and corresponding short descriptions. The agent can also send the *system* a message with the format help *tool* in order to obtain detailed help about how to use a specific tool. 

## Tools 

All interaction of the agent

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
