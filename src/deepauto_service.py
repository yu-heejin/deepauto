from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()

client = OpenAI(
  base_url="https://api.deepauto.ai/openai/v1",
  api_key=os.getenv("API"),
)

def ask_deepauto_ai():
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini-2024-07-18,deepauto/qwq-32b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "What are some highly rated restaurants in San Francisco?"
            }
        ],
        stream=True,
    )

    return completion