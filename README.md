# Code Editing Agent

> This file was written by this agent.

A simple code editing agent built in Python using Llama 3.3 70b via Groq. No frameworks, no orchestration libraries, just a while loop and a few tools.

## How it works

The agent runs a loop that talks to the model, checks if it wants to use a tool, runs the tool, sends the result back, and repeats until the model responds with text. That is all an agent is.

## Tools

- `read_file` reads the contents of a file
- `write_file` writes content to a file
- `code_execute` sandbox to execute code before pushing
- `linting` performs linting checks on the code

## Setup

```bash
pip install groq
export GROQ_API_KEY="your-key-here"
python agent.py
```

## What it can do

- Read and edit files on your machine
- Fix bugs in your code
- Create new files
- Chain multiple tool calls together to complete a task

## What it does not use

- LangChain
- LlamaIndex
- Any agent orchestration framework

Just Python and the Groq API.
