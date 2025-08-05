import asyncio

from openai import AsyncOpenAI
from fastapi import BackgroundTasks

from app.utils.file import response_to_file, read_file
from app.models.workflow_status_type import WorkflowStatusType
from app.crud.crud import update_workflow_status, create_workflow_status
from app.core.config import env_config

client = AsyncOpenAI(
    base_url=env_config.base_url,
    api_key=env_config.api_key
)

def start_workflow(background_task: BackgroundTasks):
    """
    agent를 차례대로 실행하는 workflow를 실행시킨다.
    @param background_task 에이전트를 비동기로 실행되도록 만드는 객체
    @return workflow_id 실행중인 워크플로우의 아이디
    """
    workflow_id = create_workflow_status()

    # 백그라운드에서 에이전트 실행
    background_task.add_task(run_agents, workflow_id)

    return workflow_id

async def run_agents(workflow_id: int):
    """
    agent를 순서대로 비동기식으로 실행한다.
    @param workflow_id 실행중인 워크플로우의 아이디
    """
    await data_collector_agent(workflow_id)
    await asyncio.gather(
        itinerary_builder_agent(workflow_id),
        budget_manager_agent(workflow_id),
    )
    await report_generator_agent(workflow_id)

    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.COMPLETED)

async def data_collector_agent(workflow_id: int):
    """
    Data Collector Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.DATA_COLLECTOR_START)

    system_prompt = "You are the Data Collector agent."
    user_prompt = """
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
4. Save this JSON to a file named itinerary_for_read.json.
"""
    
    chat_completion = await get_response_from_agent(system_prompt, user_prompt)
    await response_to_file(chat_completion)
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.DATA_COLLECTOR_DONE)

async def itinerary_builder_agent(workflow_id: int):
    """
    Itinerary Builder Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """

    # TODO: 두 경우 동시 실행 시 Lock 문제 확인
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.ITINERARY_AND_BUDGET_START)

    plan = read_file("itinerary_for_read.json")
    system_prompt = "You are the Itinerary Builder agent."
    user_prompt = f"""
Input:
{plan}
Task:
1. Assign days 1–5 to Tokyo → Kyoto → Osaka.
2. For each day:
    - Morning: top temple or museum visit
    - Lunch: recommended local cuisine spot
    - Afternoon: sightseeing or onsen (if weather permits)
    - Evening: transfer planning & dinner
3. Respect attraction hours and weather (e.g., rainy afternoon → indoor).
4. Output itinerary JSON:
    {{
        "day1": {{ … }},
        …,
        "day5": {{ … }}
    }}
5. Show all the steps and the reasoning process.
6. Save this JSON to a file named itinerary.json.
"""

    chat_completion = await get_response_from_agent(system_prompt, user_prompt)
    await response_to_file(chat_completion)

    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.ITINERARY_AND_BUDGET_DONE)

async def budget_manager_agent(workflow_id: int):
    """
    Budget Manager Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """

    # TODO: 두 경우 동시 실행 시 Lock 문제 확인
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.ITINERARY_AND_BUDGET_START)

    plan = read_file("itinerary_for_read.json")
    system_prompt = "You are the Budget Manager agent."
    user_prompt = f"""
Input:
```json
{plan}
```
Task:
1. Allocate 3000 USD:
    - Flights: 800 USD
    - Accommodation: 1000 USD
    - Transport (non-JR): 200 USD
    - Meals: 600 USD
    - Entrance fees: 400 USD
2. Calculate spent vs. remaining using provided prices.
3. If any category exceeds allocation:
    - Suggest cheaper 2-star hotel or local bus vs. taxi.
4. Produce budget_report JSON:
{{
    "allocated": {{ … }},
    "spent": {{ … }},
    "remaining": {{ … }},
    "alternatives": [ … ]
}}
5. Show all the steps and the reasoning process.
6. Save this JSON to a file named budget.json.
"""

    chat_completion = await get_response_from_agent(system_prompt, user_prompt)
    await response_to_file(chat_completion)
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.ITINERARY_AND_BUDGET_DONE)

async def report_generator_agent(workflow_id: int):
    """
    Report Generator Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.REPORT_GENERATOR_START)

    itinerary = read_file("itinerary.json")
    budget = read_file("budget.json")

    system_prompt = (
        "You are the Report Generator agent. "
        "When you produce your final output, only respond by calling the save_to_file function; "
        "do not emit any other plain-text response."
    )
    user_prompt = f"""
Input:
itinerary: 
{itinerary}
budget_report: 
{budget}
Task:
1. Combine the two JSONs into a single report.
2. Include sections:
    - Trip Overview (2025-10-01 to 2025-10-05, route, total_budget)
    - Day-by-Day Itinerary (with times, locations, notes)
    - Budget Summary Table (allocated/spent/remaining)
    - Reservation Checklist (flight#, hotel names, JR Pass)
    - Packing & Pre-departure Reminders
3. Highlight:
    - Cost-saving tips
    - Must-see spots
    - Onsen & temple visit recommendations
4. Show all the steps and the reasoning process.
5. Save the report to a file named report.md.
"""
    chat_completion = await get_response_from_agent(system_prompt, user_prompt)
    await response_to_file(chat_completion)
    
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.REPORT_GENERATOR_DONE)
    
async def get_response_from_agent(system_prompt: str, user_prompt: str):
    return await client.chat.completions.create(
        model="openai/gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt
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