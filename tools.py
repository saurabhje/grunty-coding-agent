import os
import subprocess
agent_tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The relative file path"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Use this tool only when you are creating a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The relative file path"},
                    "content": {"type": "string", "description": "The content to write"}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "use this method to edit or make changes to a file by replacing a specific string with a new string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The relative file path"},
                    "old_str": {"type": "string", "description": "String to be replaced"},
                    "new_str": {"type": "string", "description": "Replacement string"}
                },
                "required": ["filepath", "old_str", "new_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in a directory recursively. Use this first to understand the codebase structure. Skip the files that are result of build, cache or library modules",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Root directory to start the walk. Defaults to current directory."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return the output. Use this to run code, tests, or linters after making changes to verify nothing is broken.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"]
            }
            
        }
    }
]


def read_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"File Error: {e}"

def write_file(filepath: str, content: str):
    try:
        if os.path.exists(filepath):
            return f"Error: {filepath} already exists. Use edit_file to modify existing files."
        with open(filepath, "w") as f:
            f.write(content) 
            return f"Successfully written: {filepath}"
    except Exception as e:
        return f"Writing error: {e}"

def edit_file(filepath: str, old_str: str, new_str: str):
    try:
        with open(filepath, "r") as f:
            content = f.read()
        if old_str not in content:
            return f"Error: the specified string not in content, current file content: {content}"
        new_content = content.replace(old_str, new_str)
        with open(filepath, "w") as f:
            f.write(new_content)

        return f"Successfully edited {filepath}"
    except Exception as e:
        return f"unsuccessful at editing: {e}"
    
def list_files(directory: str = "."):
    try:
        files = []
        for root, dirs, filenames in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", ".venv", "dist", "build")]
            for file in filenames:
                filepath = os.path.join(root, file)
                files.append(filepath)
                if len(files) > 100:
                    return f"\n{files}\n truncated.."
        return f"\n{files}"
    except Exception as e:
        return f"error reading file: {e}"

def run_command(command: str):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return f"FAILED (exit {result.returncode}):\n{result.stderr or result.stdout}\nFix the error and run again."
        return result.stdout or "command produced no output"
    except subprocess.TimeoutExpired:
        return f"comamnd timed out after 30 seconds"
    except Exception as e:
        return f"error enocuntered: {e}"
    
tools_map = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "list_files": list_files,
    "run_command": run_command
}
