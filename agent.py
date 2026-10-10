import json
import os
from unittest import result
from openai import OpenAI
from project_tools import see_file_tree
from project_tools import read_file

api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)
model = "gpt-6-luna"  # or your preferred model

# Tool schema
see_file_tree_description = {
    "type": "function",
    "name": "see_file_tree",
    "description": "List files and directories in the project.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directory path to list. Defaults to '.'.",
            }
        },
        "required": [],
        "additionalProperties": False,
    },
    "strict": False,
}

#read a file schema
read_file_description = {
    "type": "function",
    "name": "read_file",
    "description": "Read the contents of a file in the current project.",
    "parameters": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Path to the file to read.",
            }
        },
        "required": ["filepath"],
        "additionalProperties": False,
    },
}

#for future use, we can map the tool names to their corresponding functions
#result = tools_map[func_name](**func_args)
tools_map = {
    "see_file_tree": see_file_tree,
    "read_file": read_file
}


user_prompt = "What dependencies does this project have?"
system_prompt = "You are a helpful assistant that can analyze the project structure and read files to answer questions about the project."

chat_messages = [
    {"role": "developer", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

# 1. Ask model
response = openai_client.responses.create(
    model=model,
    input=chat_messages,
    tools=[see_file_tree_description, read_file_description]
)




#Append the tool call and result like this. 
chat_messages = [
    {"role": "developer", "content": system_prompt}
]

while True:
    user_prompt = input(">> ").strip()
    if user_prompt.lower() == "stop":
        print("Chat ended.")
        break

    chat_messages.append({"role": "user", "content": user_prompt})

    while True:
        response = openai_client.responses.create(
            model=model,
            input=chat_messages,
            tools=[see_file_tree_description, read_file_description]
        )

        has_tool_calls = False

        for item in response.output:
            chat_messages.append(item)

            if item.type == 'function_call':
                has_tool_calls = True
                f_name = item.name
                args = json.loads(item.arguments)
                print(f'tool_call: {f_name}({args})')

                if f_name == 'see_file_tree':
                    result = see_file_tree(**args)
                elif f_name == 'read_file':
                    result = read_file(**args)
                else:
                    result = {'error': f'unknown function {f_name}'}

                chat_messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result),
                })
            elif item.type == 'message':
                print(item.content[0].text)

        if not has_tool_calls:
            break