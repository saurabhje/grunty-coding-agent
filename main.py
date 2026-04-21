import os
import json
import sys
from groq import Groq
from tools import agent_tools, tools_map

client = Groq(api_key=os.environ["GROQ_API_KEY"])

MAX_CONTEXT = 20
def run():
    try:
        conversations = [
            {
                "role": "system",
                "content": """You are a senior software engineer and coding agent. You have access to tools to read_file, write_file, list_files, edit_files and run_commands only do not use any other tool.
                        Keep responses concise and technical. No emojis. No filler phrases like 'Great question' or 'Certainly'.
                        After making changes to the code, don't return entire change. Simple changelog description will be fine. Return plain text only. No markdown, no code blocks, no asterisks, no headers.
                        """
            }
        ]

        while True:
            user_input = input("\033[94mYou\033[0m: ")
            if user_input.strip().lower() == "/clear":
                conversations = conversations[:1]
                print("context cleared, all conversations deleted")
                continue
            conversations.append({"role": "user", "content": user_input})

            while True:
                try:
                    trimmed = [conversations[0]] + conversations[-MAX_CONTEXT:]
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=trimmed,
                        tools=agent_tools,
                    )
                    message = response.choices[0].message

                    if message.tool_calls:
                        conversations.append(
                            {"role": "assistant", "content": message.content, "tool_calls": message.tool_calls}
                        )

                        for tool_call in message.tool_calls:
                            tool_name = tool_call.function.name
                            tool_args = json.loads(tool_call.function.arguments)
                            print(f"\033[92mcalling tool\033[0m: {tool_name}")
                            result = tools_map[tool_name](**tool_args)
                            conversations.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "name": tool_name,
                                    "content": result,
                                }
                            )
                    else:
                        reply = message.content
                        print(f"\u001b[93mGrunter\u001b[0m: {reply}")
                        conversations.append({"role": "assistant", "content": reply})
                        break

                except Exception as e:
                    print(f"\033[91merror\033[0m: {e}\n")
                    break

    except KeyboardInterrupt:
        print("\nBye")
        sys.exit(0)
run()