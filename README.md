# Grunty - Code Editing Agent

A minimal code editing agent built in Python using gpt-oss-120b via Groq. No frameworks, no orchestration libraries, just a while loop and a few tools.

## How it works

The agent runs a loop that talks to the model, checks if it wants to use a tool, runs the tool, sends the result back, and repeats until the model responds with text. That is all an agent is.

## Tools

- `read_file` reads the contents of a file
- `write_file` creates or overwrites a file with new content
- `edit_file` makes precise changes to a file by replacing a specific string with a new one
- `list_files` lists all files in a directory recursively
- `run_command` runs a shell command and returns the output, used for running code, tests, and linters

## Setup

Clone the repo and install:

```bash
git clone https://github.com/saurabhje/grunty-coding-agent
cd grunty-coding-agent
uv tool install .
```

Set your Groq API key. Get one free at https://console.groq.com:

```bash
export GROQ_API_KEY="your-key-here"
```

To make the key permanent add it to your ~/.bashrc or ~/.zshrc:

```bash
echo 'export GROQ_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

Navigate to any codebase and run:

```bash
cd /path/to/your/project
grunty
```

Type `clear` to reset the conversation context. Ctrl+C to quit.

## What it can do

- Explore a codebase by listing and reading files
- Create new files and edit existing ones
- Fix bugs and make precise code changes
- Run commands to verify changes did not break anything
- Chain multiple tool calls together to complete a task autonomously

## What it does not use

- LangChain
- LlamaIndex
- Any agent orchestration framework

Just Python and the Groq API.