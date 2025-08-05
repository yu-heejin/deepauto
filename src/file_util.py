import json
from datetime import datetime

async def response_to_file(chat_completion):
    result = ""
    
    async for chat in chat_completion:
        delta = chat.choices[0].delta

        if delta.tool_calls is not None and delta.tool_calls[0].function is not None:
            result += delta.tool_calls[0].function.arguments or ""

        if chat.choices[0].delta.content is not None:
            print(chat.choices[0].delta.content, end="")

    result_json = json.loads(result)

    with open(result_json["filename"], "w", encoding="utf-8") as f:
        f.write(result_json["content"])

    print(f"✅ File saved to {result_json['filename']}, time: {datetime.now()}")

def read_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()