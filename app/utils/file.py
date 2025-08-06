import json
import os
import aiofiles
import asyncio

from datetime import datetime
from pathlib import Path

async def save_to_file(response):
    """
    json 응답을 파일로 변환해 저장하는 함수
    @param response json 객체
    """
    with open(response["filename"], "w", encoding="utf-8") as f:
        f.write(response["content"])

    print(f"✅ File saved to {response['filename']}, time: {datetime.now()}")

async def read_file(path: str):
    """
    파일 내용을 읽는 비동기 함수
    @param path 파일 경로
    """
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        return await f.read()
    
async def to_json(chat_completion):
    """
    에이전트 클라이언트 응답을 JSON으로 변환하는 함수
    @param chat_completion 에이전트 응답
    """
    result = ""

    async for chat in chat_completion:
        delta = chat.choices[0].delta

        if delta.tool_calls is not None and delta.tool_calls[0].function is not None:
            result += delta.tool_calls[0].function.arguments or ""

        if chat.choices[0].delta.content is not None:
            print(chat.choices[0].delta.content, end="")

    if not result:
        raise ValueError("[ERROR] result가 없습니다.")

    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        # 디버깅을 위해 누적된 문자열을 함께 띄워 줍니다
        raise ValueError(f"[ERROR] JSON Parssing Error: {e.msg}") from e