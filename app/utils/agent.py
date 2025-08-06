import asyncio
from datetime import datetime

from openai import AsyncOpenAI
from fastapi import BackgroundTasks

from app.utils.file import save_to_file, read_file, to_json
from app.models.workflow_status_type import WorkflowStatusType
from app.models.workflow_agent_type import WorkflowAgentType
from app.crud.crud import update_workflow_status, create_workflow_status, create_workflow_agent_response, create_workflow_agent, update_workflow_agent_status
from app.core.config import env_config
from app.utils.websocket import (
    broadcast_agent_status, 
    broadcast_agent_complete_response,
    broadcast_workflow_status,
    broadcast_to_workflow
)

def create_client():
    """
    OpenAI 클라이언트 생성
    @return AsyncOpenAI 객체
    """
    return AsyncOpenAI(
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
    try:
        # Workflow 시작 상태 브로드캐스트
        await broadcast_workflow_status(workflow_id, WorkflowStatusType.RUNNING)
        update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.RUNNING)
        
        await data_collector_agent(workflow_id)
        await asyncio.gather(
            itinerary_builder_agent(workflow_id),
            budget_manager_agent(workflow_id),
        )
        await report_generator_agent(workflow_id)
    except Exception as e:
        print(f"[ERROR] {e}")
        update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.FAILED)
        await broadcast_workflow_status(workflow_id, WorkflowStatusType.FAILED)
        return
    
    # Workflow 완료 상태 브로드캐스트
    update_workflow_status(workflow_id=workflow_id, status=WorkflowStatusType.COMPLETED)
    await broadcast_workflow_status(workflow_id, WorkflowStatusType.COMPLETED)

async def data_collector_agent(workflow_id: int):
    """
    Data Collector Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """

    try:
        agent_id = create_workflow_agent(
            workflow_id=workflow_id, 
            agent_name=WorkflowAgentType.DATA_COLLECTOR,
            status=WorkflowStatusType.RUNNING
        )
        await broadcast_agent_status(workflow_id, WorkflowAgentType.DATA_COLLECTOR, WorkflowStatusType.RUNNING)
        
        # Agent 시작 상태 브로드캐스트
        
        system_prompt = "You are the Data Collector agent."
        user_prompt = f"""
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
        {{
            "preferences": {{ …fixed… }},
            "flights": [ … ],
            "hotels": [ … ],
            "transport": {{ … }},
            "attractions": [ … ],
            "weather": [ … ]
        }}
    3. Show all the steps and the reasoning process.
    4. Save this JSON to a file named {f'itinerary_for_read_{workflow_id}.json'}.
    5. Save this JSON to a file named "{f'itinerary_for_read_{workflow_id}.json'}" and do not call the function again.  
    """
        
        chat_completion = await get_response_from_agent(system_prompt, user_prompt)
        response = await to_json(chat_completion)
        if response is None:
            update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.DATA_COLLECTOR, WorkflowStatusType.FAILED)
        else:
            await save_to_file(response=response)
            await asyncio.gather(
                asyncio.to_thread(create_workflow_agent_response, workflow_id, agent_id, response_data=response),
                asyncio.to_thread(update_workflow_agent_status, agent_id, WorkflowStatusType.COMPLETED),
            )
            
            # 완료된 응답 브로드캐스트
            await broadcast_agent_complete_response(workflow_id, WorkflowAgentType.DATA_COLLECTOR, response)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.DATA_COLLECTOR, WorkflowStatusType.COMPLETED)
    except Exception as e:
        update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
        await broadcast_agent_status(workflow_id, WorkflowAgentType.DATA_COLLECTOR, WorkflowStatusType.FAILED)
        raise Exception(f"[ERROR] Data Collector Agent Error: {e}")

async def itinerary_builder_agent(workflow_id: int):
    """
    Itinerary Builder Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """

    try:
        agent_id = create_workflow_agent(
            workflow_id=workflow_id, 
            agent_name=WorkflowAgentType.ITINERARY_BUILDER,
            status=WorkflowStatusType.RUNNING
        )
        # Agent 시작 상태 브로드캐스트
        await broadcast_agent_status(workflow_id, WorkflowAgentType.ITINERARY_BUILDER, WorkflowStatusType.RUNNING)

        plan = await read_file(f"itinerary_for_read_{workflow_id}.json")
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
    6. Save this JSON to a file named {f'itinerary_{workflow_id}.json'}.
    7. Save this JSON to a file named "{f'itinerary_{workflow_id}.json'}." and do not call the function again.
    """
        
        chat_completion = await get_response_from_agent(system_prompt, user_prompt)
        response = await to_json(chat_completion=chat_completion)
        
        if response is None:
            update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.ITINERARY_BUILDER, WorkflowStatusType.FAILED)
        else:
            await save_to_file(response=response)
            # 에이전트 응답 저장
            await asyncio.gather(
                asyncio.to_thread(create_workflow_agent_response, workflow_id, agent_id, response_data=response),
                asyncio.to_thread(update_workflow_agent_status, agent_id, WorkflowStatusType.COMPLETED),
            )
            
            # 완료된 응답 브로드캐스트
            await broadcast_agent_complete_response(workflow_id, WorkflowAgentType.ITINERARY_BUILDER, response)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.ITINERARY_BUILDER, WorkflowStatusType.COMPLETED)
    except Exception as e:
        update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
        await broadcast_agent_status(workflow_id, WorkflowAgentType.ITINERARY_BUILDER, WorkflowStatusType.FAILED)
        raise Exception(f"[ERROR] Itinerary Builder Agent Error: {e}")

async def budget_manager_agent(workflow_id: int):
    """
    Budget Manager Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """

    try:
        agent_id = create_workflow_agent(
            workflow_id=workflow_id, 
            agent_name=WorkflowAgentType.BUDGET_MANAGER,
            status=WorkflowStatusType.RUNNING
        )
        # Agent 시작 상태 브로드캐스트
        await broadcast_agent_status(workflow_id, WorkflowAgentType.BUDGET_MANAGER, WorkflowStatusType.RUNNING)

        plan = await read_file(f"itinerary_for_read_{workflow_id}.json")
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
    6. Save this JSON to a file named {f'budget_{workflow_id}.json'}.
    7.Save this JSON to a file named "{f'budget_{workflow_id}.json'}." and do not call the function again.
    """
        chat_completion = await get_response_from_agent(system_prompt, user_prompt)    
        response = await to_json(chat_completion=chat_completion)
        
        if response is None:
            update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.BUDGET_MANAGER, WorkflowStatusType.FAILED)
        else:
            await save_to_file(response=response)
            await asyncio.gather(
                asyncio.to_thread(create_workflow_agent_response, workflow_id, agent_id, response_data=response),
                asyncio.to_thread(update_workflow_agent_status, agent_id, WorkflowStatusType.COMPLETED),
            )
            
            # 완료된 응답 브로드캐스트
            await broadcast_agent_complete_response(workflow_id, WorkflowAgentType.BUDGET_MANAGER, response)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.BUDGET_MANAGER, WorkflowStatusType.COMPLETED)
    except Exception as e:
        update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
        await broadcast_agent_status(workflow_id, WorkflowAgentType.BUDGET_MANAGER, WorkflowStatusType.FAILED)
        raise Exception(f"[ERROR] Budget Manager Agent Error: {e}")

async def report_generator_agent(workflow_id: int):
    """
    Report Generator Agent 실행 함수
    @param workflow_id 실행중인 워크플로우의 아이디
    """

    try:
        agent_id = create_workflow_agent(
            workflow_id=workflow_id, 
            agent_name=WorkflowAgentType.REPORT_GENERATOR,
            status=WorkflowStatusType.RUNNING
        )
        # Agent 시작 상태 브로드캐스트
        await broadcast_agent_status(workflow_id, WorkflowAgentType.REPORT_GENERATOR, WorkflowStatusType.RUNNING)

        itinerary = await read_file(f"itinerary_{workflow_id}.json")
        budget = await read_file(f"budget_{workflow_id}.json")

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
    5. Save the report to a file named {f'report_{workflow_id}.md'}.
    6. Save this JSON to a file named "{f'report_{workflow_id}.md'}." and do not call the function again.
    """
        
        chat_completion = await get_response_from_agent(system_prompt, user_prompt)
        response = await to_json(chat_completion=chat_completion)

        if response is None:
            update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.REPORT_GENERATOR, WorkflowStatusType.FAILED)
        else:
            await save_to_file(response=response)
            await asyncio.gather(
                asyncio.to_thread(create_workflow_agent_response, workflow_id, agent_id, response_data=response),
                asyncio.to_thread(update_workflow_agent_status, agent_id, WorkflowStatusType.COMPLETED),
            )
            
            # 완료된 응답 브로드캐스트
            await broadcast_agent_complete_response(workflow_id, WorkflowAgentType.REPORT_GENERATOR, response)
            await broadcast_agent_status(workflow_id, WorkflowAgentType.REPORT_GENERATOR, WorkflowStatusType.COMPLETED)
            
            # 결과 보고서 출력
            report_content = await read_file(f"/deepauto/report_{workflow_id}.md")
            if report_content:
                # 보고서를 웹소켓으로 실시간 전송
                report_data = {
                    "workflow_id": workflow_id,
                    "report": report_content,
                    "timestamp": datetime.now().isoformat()
                }
                await broadcast_to_workflow(workflow_id, report_data)
    except Exception as e:
        update_workflow_agent_status(agent_id, WorkflowStatusType.FAILED)
        await broadcast_agent_status(workflow_id, WorkflowAgentType.REPORT_GENERATOR, WorkflowStatusType.FAILED)
        raise Exception(f"[ERROR] Report Generator Agent Error: {e}")

async def get_response_from_agent(system_prompt: str, user_prompt: str):
    """
    에이전트로 부터 응답을 받는 클라이언트 함수
    @param system_prompt 역할 프롬프트
    @param user_prompt 명령 프롬프트
    """
    client = create_client()
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