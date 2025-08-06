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

    async for chunk in chat_completion:
        if not chunk.choices:
            continue
            
        delta = chunk.choices[0].delta

        # tool_calls 처리 (현재 OpenAI API 표준)
        if getattr(delta, "tool_calls", None):
            for call in delta.tool_calls:     
                if getattr(call, "function", None) and getattr(call.function, "arguments", None):
                    result += call.function.arguments
        
        # 일반 텍스트 출력 (디버깅용)
        if delta.content:
            print(delta.content, end="")

    if not result:
        raise ValueError("[ERROR] result가 없습니다.")

    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        # 디버깅을 위해 누적된 문자열을 함께 띄워 줍니다
        raise ValueError(f"[ERROR] JSON Parssing Error: {e.msg}") from e