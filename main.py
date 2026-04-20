import os
import json
import sys
from groq import Groq
from tools import agent_tools, tools_map

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def run():
    conversations = [
        {
            "role": "system",
            "content": """You are a senior software engineer and coding agent. 
                    You have access to tools to read, write, list files, edit files and run commands on the user's machine.
                    Keep responses concise and technical. No emojis. No filler phrases like 'Great question' or 'Certainly'.
                    After making changes to the code, don't return entire change. Simple changelog description will be fine.
                    """
        }
    ]

    while True:
        user_input = input("\033[94mYou\033[0m: ")
        conversations.append({"role": "user", "content": user_input})

        while True:
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=conversations,
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
                    print(f"\u001b[93mGrunter\u001b[0m: {reply}\n")
                    conversations.append({"role": "assistant", "content": reply})
                    break

            except Exception as e:
                print(f"\033[91merror\033[0m: {e}\n")
                break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nBye")
        sys.exit(0)