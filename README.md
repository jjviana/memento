Disclaimer: documentation generated in collaboration with [claude.ai](https://claude.ai/chat)

# Memento

Memento is a framework for building customizable AI agents that can complete complex tasks by combining simple modular tools. It allows creating assistants that can understand natural language requests, decompose them into simpler subtasks, and leverage existing tools and skills to satisfy user needs. It is not a production-ready tool by any means, but a framework to investigate reasoning and planning capabilities of large language models. 

## Where does the name 'Memento' comes from?

[Memento](https://en.wikipedia.org/wiki/Memento_(film)) is a movie by Christoper Nolan, where the main character (Leonard Shelby) suffers from short-term memory loss. Leonard manages to put together a functioning personality by continuously reading notes left by himself, acting on the information present in these notes and then writing new notes for his future self. 

Large language models (as of mid-2023) also have very limited short-term memory. Memento (the software package) is an experiment in teaching these models to overcome that limitation in a way similar to the character Leonard Shelby.

## Main results so far

- GPT-3.5-turbo is capable of handling moderately complex requests, but usually fails when the requests requires long multi-step reasoning chains. The most common failure mode is the agent gettng stuck into a loop, executing the same commands again and again. Careful prompting avoids that sometimes, but not always.
- GPT-4 seems to be able to handle complex requests without problems. See the Yelb experiment example for details fo how GPT-4 can understand a simple codebase even in the absence of any auxiliary systems such as semantic indexes.

## Running
- Install dependencies: pip install -r requirements.txt
- change to a bot directory (i.e. ``cd bots/adventure``)
- run: python ../../memento.py

The first time it is run, memento will ask for a valid OpenAI account ID. 

## Overview

The core ideas behind Memento are:

- **Composability** - Complex behaviors are built by combining simple, single-purpose tools.
- **Language-centric** - All interaction happens through natural language. Agents and tools communicate via messages.
- **Tool abstraction** - Tools provide a simple interface and can be anything from shell scripts to sophisticated ML models.
- **Scalable reasoning** - Language models like GPT-3 handle composing behaviors, even as the set of available skills grows.

At a high level, Memento agents accept natural language requests from users, break them down into subtasks if needed, call the appropriate tools to execute those subtasks, then compose the results and report back to the user.

The system has four main components:

### Language Models

Large language models handle the natural language processing and reasoning required for the agent to understand requests, plan, call tools, and compose responses. Currently  GPT-3.5 and GPT-4 are supported, other models will be tried as I can get access to them.

### Tools

Self-contained scripts or programs that each provide a simple skill or capability. Tools connect to the agent via a simple messaging protocol. Both subprocess tools (shell scripts) and tools powered by subordinate Memento agents are supported.

### Prompts

Prompt templates prime the language model to play its role in the Memento framework. Prompts load condition the model on the messaging protocol, tool invocation syntax, and other conventions.

### Tools Manager

Keeps track of available tools and handles invoking the correct one based on agent requests. Includes common tools like help and tool discovery.

## Agent Architecture

At runtime, a Memento agent consists of:

- A Language Model instance that handles conversation and reasoning
- A Tools Manager that tracks and invokes available tools 
- A Prompts Manager that provides prompt templates

To create an agent, these components are instantiated and connected:

```python
prompts_manager = PromptsManager()
tools_manager = ToolsManager() 

model = GPT3()
agent = Memento(tools_manager, prompts_manager, model)
```

The main agent class glues everything together. When a user request comes in:

1. The agent formats it and feeds it into the language model 
2. The model outputs a tool invocation message
3. The Tools Manager runs the tool and captures the result
4. The output is sent back to the model to incorporate into the final response
5. The final response is returned to the user

So at a high level, the language model and tools manager work together to break down and satisfy complex requests.

## Tool Development

One of the key ideas in Memento is that new behaviors are added by creating small, focused tools. Some hypothetical examples:

- `calendar.sh`: a shell script that exposes calendar operations 
- `weather.py`: a Python module that returns weather forecasts 
- `travel_agent.py`: a subordinate Memento agent that books flights and hotels 

Tools connect to the main agent using stdin/stdout messaging. For example:

```
{{FROM:agent TO:calendar}}
list_meetings
{{END}}

{{FROM:calendar TO:agent}}
Team meeting 10am Monday
1-on-1 2pm Wednesday  
{{END}}
```

So tools can be created with any language or framework, as long as they can send and receive messages over stdin/stdout.

## Usage Examples

Some examples are include in the `bots` directory:
 - adventure: a simple text adventure game
 - email_client: acconversational email client
 - coder: a bot capable of interacting with source code


