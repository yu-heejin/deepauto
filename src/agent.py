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

def data_collector_agent():
    chat_completion = client.chat.completions.create(
        model="openai/gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are the Data Collector agent."},
            {
                "role": "user",
                "content": """
Input:
```json
total_budget: 3000 USD
preferred_route: ["Tokyo", "Kyoto", "Osaka"]
accommodation_type: "3-star hotel"
travel_dates:
start_date: "2025-10-01"
end_date: "2025-10-05"
special_interests: ["onsen", "local cuisine", "temple visits"]
```
Task:
1. Using the fixed input above, fetch via APIs or web scraping:
    - Round-trip flights (ICN ⇄ NRT/KIX)
    - 3-star hotels in each city
    - JR Pass cost and regional transfers
    - Major attraction hours, public holidays, and festival dates
    - 5-day weather forecasts for Tokyo, Kyoto, Osaka
2. Aggregate into JSON:
    {
        "preferences": { …fixed… },
        "flights": [ … ],
        "hotels": [ … ],
        "transport": { … },
        "attractions": [ … ],
        "weather": [ … ]
    }
3. Show all the steps and the reasoning process.
4. Save this JSON to a file named itinerary.json.
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

def itinerary_builder_agent():
    file_path = "/deepauto/itinerary.json"
    chat_completion = client.chat.completions.create(
        model="openai/gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are the Itinerary Builder agent."},
            {
                "role": "user",
                "content": """
Input:
/deepauto/itinerary.json
Task:
1. Assign days 1–5 to Tokyo → Kyoto → Osaka.
2. For each day:
    - Morning: top temple or museum visit
    - Lunch: recommended local cuisine spot
    - Afternoon: sightseeing or onsen (if weather permits)
    - Evening: transfer planning & dinner
3. Respect attraction hours and weather (e.g., rainy afternoon → indoor).
4. Output itinerary JSON:
    
    {
    
    "day1": { … },
    
    …,
    
    "day5": { … }
    
    }
    

5. Show all the steps and the reasoning process.
6. Save this JSON to a file named itinerary.json.
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
