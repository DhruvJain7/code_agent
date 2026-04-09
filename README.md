# 🤖 code_agent

A toy agentic code editor in Python — inspired by tools like **Claude Code** and **Cursor's Agent Mode**. You give it a coding task in plain English, and it autonomously explores your codebase, reads files, writes fixes, runs the code, and iterates until the task is done.

Powered by **Google Gemini 2.5 Flash** via the `google-genai` SDK.

---

## How It Works

The agent runs in a loop (up to 20 iterations) and is given four tools it can call autonomously:

| Tool | What It Does |
|---|---|
| `get_files_info` | Lists files and directories in the working directory |
| `get_file_content` | Reads the contents of a specific file |
| `write_file` | Writes or overwrites a file with new content |
| `run_python_file` | Executes a Python file and returns the output |

On each iteration, Gemini decides which tool to call based on the task. It reads context, forms a plan, makes changes, runs the code, and checks the output — all without human input. When it's satisfied the task is complete, it prints a final response and exits.

The agent operates on a fixed **working directory** (`./calculator` by default), keeping it sandboxed from the rest of your filesystem.

---

## Project Structure

```
code_agent/
├── main.py                   # Entry point — CLI, Gemini loop, tool dispatch
├── call_function.py          # Registers tools and routes function calls
├── prompts.py                # System prompt that governs agent behaviour
├── config.py                 # Configuration constants
├── functions/
│   ├── get_files_info.py     # List directory contents
│   ├── get_files_content.py  # Read a file
│   ├── write_files.py        # Write/overwrite a file
│   └── run_python_file.py    # Execute a Python file
├── calculator/               # Sample working directory for the agent
├── test_get_file_content.py
├── test_get_files_info.py
├── test_run_python_file.py
├── test_write_file.py
└── pyproject.toml
```

---

## Prerequisites

- Python 3.13+
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`
- A **Google Gemini API key** — get one free at [aistudio.google.com](https://aistudio.google.com/)

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/DhruvJain7/code_agent.git
cd code_agent
```

**2. Install dependencies**

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

**3. Set up your API key**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

```bash
python main.py "<your task here>"
```

**Example:**

```bash
python main.py "There's a bug in the calculator — strings aren't splitting correctly. Find and fix it."
```

**With verbose output** (shows each function call result):

```bash
python main.py "Add a multiply function to the calculator" --verbose
```

**What you'll see:**

```
Calling function: get_files_info({'directory': '.'})
Calling function: get_file_content({'file_path': 'calculator.py'})
Calling function: write_file({'file_path': 'calculator.py', 'content': '...'})
Calling function: run_python_file({'file_path': 'calculator.py'})
Agent: I've fixed the string splitting bug. The issue was in line 12 where...
User prompt: There's a bug in the calculator...
Prompt tokens: 1423
Response tokens: 312
```

---

## Agent Behaviour

The system prompt instructs the agent to follow these rules on every task:

- **Plan before acting** — explicitly states its step-by-step plan before making any function calls
- **Read before writing** — always reads a file before modifying it
- **Iterate step-by-step** — evaluates output from each action before deciding the next move
- **Handle errors gracefully** — reads error messages, adjusts the plan, and retries with a different approach rather than repeating failed calls
- **Use relative paths only** — the working directory is injected automatically for safety

---

## Running Tests

Individual tool functions have their own test files:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_write_file.py
python test_run_python_file.py
```

---

## Configuration

The working directory is currently hardcoded to `./calculator` in `call_function.py`:

```python
args["working_directory"] = "./calculator"
```

To point the agent at a different project, update this path before running.

---

## Dependencies

| Package | Version |
|---|---|
| `google-genai` | 1.12.1 |
| `python-dotenv` | 1.1.0 |

---

## Limitations

- The agent targets a single fixed working directory per run
- Maximum of 20 agentic iterations per task
- No persistent memory between runs
- Only supports Python files for execution

---

## Acknowledgements

Built as a learning project to understand how agentic coding tools like Claude Code and Cursor's Agent Mode work under the hood — function-calling loops, tool routing, and autonomous iteration over a codebase.

---

*Made by [Dhruv Jain](https://github.com/DhruvJain7)*
