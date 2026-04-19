import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def read_file(filepath: str):
    """
    reads the content of a file with specified file path
    parameter: filepath, a string to specify which file to read
    """
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"File Error: {e}"

def write_file(filepath: str, content: str):
    """
    writes back the content to the specified filepath
    parameter: filepath (where to write), content(what to write)
    """
    try:
        with open(filepath, "w") as f:
            f.write(content) 
            return f"Successfully written: {filepath}"
    except Exception as e:
        return f"Writing error: {e}"
    

agent_tools =  [read_file, write_file]
tools_map = {
    "read_file": read_file,
    "write_file": write_file
}

def run():
    conversations = []

    while True:
        user_input = input("\033[94mYou\033[0m: ")
        conversations.append(
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        )
        while True:
            try:
                response = client.models.generate_content(
                    model="gemini-3.1-preview",
                    contents=conversations,
                    config=types.GenerateContentConfig(
                        tools=agent_tools
                    )
                )
                if response.function_calls:
                    conversations.append({"role": "model", "parts": response.candidates[0].content.parts })

                    tool_result = []
                    for tool_call in response.function_calls:
                        tool_name = tool_call.name
                        tool_args = tool_call.args

                        result = tools_map[tool_name](**tool_args)
                    
                        tool_result.append(types.Part.from_function_response(name=tool_name, response={"result": result}))    

                    conversations.append({
                        "role": "user",
                        "parts": tool_result
                    })
                else:
                    reply = response.text
                    print(f"\u001b[93mGemini\u001b[0m: {reply}\n")
                    conversations.append({"role": "model", "parts": [{"text": reply}]})
                    break
            
            except Exception as e:
                print(f"\033[91merror\033[0m: {e.message}\n")
                break


run()