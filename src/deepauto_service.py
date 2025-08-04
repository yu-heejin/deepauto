from openai import OpenAI
from dotenv import load_dotenv
from src.file_util import save_file

import os
import json

load_dotenv()

client = OpenAI(
  base_url="https://api.deepauto.ai/openai/v1",
  api_key=os.getenv("API"),
)

def ask_deepauto_ai():
    chat_completion = client.chat.completions.create(
        model="openai/gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": """
    What are some highly rated restaurants in San Francisco?
    Show all the steps and the reasoning process and Save report to a file named sanfrancisco.md.
    """,
            },
        ],
        tool_choice="auto",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "save_to_file",
                    "description": "Save content to a local file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "The name of the file to save to"},
                            "content": {"type": "string", "description": "The content to write into the file"},
                        },
                        "required": ["filename", "content"],
                    },
                },
            }
        ],
        stream=True,
    )

    result = ""
    for chat in chat_completion:
        delta = chat.choices[0].delta

        if delta.tool_calls is not None and delta.tool_calls[0].function is not None:
            result += delta.tool_calls[0].function.arguments or ""

        if chat.choices[0].delta.content is not None:
            print(chat.choices[0].delta.content, end="")

    result_json = json.loads(result)
    save_file(result_json["filename"], result_json["content"])