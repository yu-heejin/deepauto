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
    # result = ""
    
    # async for chat in chat_completion:
    #     delta = chat.choices[0].delta

    #     if delta.tool_calls is not None and delta.tool_calls[0].function is not None:
    #         result += delta.tool_calls[0].function.arguments or ""

    #     if chat.choices[0].delta.content is not None:
    #         print(chat.choices[0].delta.content, end="")

    # result_json = json.loads(result)
    # return result_json

    result = ""

    async for chunk in chat_completion:
        delta = chunk.choices[0].delta

        # tool_calls 처리 (현재 OpenAI API 표준)
        if getattr(delta, "tool_calls", None):
            for call in delta.tool_calls:
                if getattr(call, "function", None) and getattr(call.function, "arguments", None):
                    result += call.function.arguments
        if delta.content:
            print(delta.content, end="")

    if not result:
        raise ValueError("LLM이 함수 호출을 통해 JSON을 반환하지 않았습니다.")

    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        # 디버깅을 위해 누적된 문자열을 함께 띄워 줍니다
        raise ValueError(f"JSON 파싱 실패: {e.msg}\n원본: {result!r}") from e