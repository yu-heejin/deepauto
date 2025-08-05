import json

from datetime import datetime

async def save_to_file(response):
    with open(response["filename"], "w", encoding="utf-8") as f:
        f.write(response["content"])

    print(f"✅ File saved to {response['filename']}, time: {datetime.now()}")

def read_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
async def to_json(chat_completion):
    result = ""
    
    async for chat in chat_completion:
        delta = chat.choices[0].delta

        if delta.tool_calls is not None and delta.tool_calls[0].function is not None:
            result += delta.tool_calls[0].function.arguments or ""

        if chat.choices[0].delta.content is not None:
            print(chat.choices[0].delta.content, end="")

    result_json = json.loads(result)
    return result_json
