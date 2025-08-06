# Multi Agent Workflow System 구현

## 사용 기술

- FastAPI + Python (3.11)
- MySQL
- Docker
- docker-compose

## 실행 방법

1. 현재 repository 상위에 .env 파일 생성

2. 명령어 실행

```
docker-compose up -d
```

* 소스 코드나 파일에 변경이 생긴 경우, 아래 명령어 실행

```
docker-compose up -d --build
```

## API 실행 결과

`POST /workflows` 

### Response

```json
{
    "status": 201,
    "data": {
        "id": 2
    }
}
```

### Database 실행 결과

```bash
mysql> select * from workflow_agent;
+----+-------------+-------------------------+-----------+---------------------+---------------------+
| id | workflow_id | agent_name              | status    | created_at          | updated_at          |
+----+-------------+-------------------------+-----------+---------------------+---------------------+
|  1 |           1 | DATA_COLLECTOR_AGENT    | FAILED    | 2025-08-05 14:35:29 | 2025-08-05 14:35:31 |
|  2 |           1 | ITINERARY_BUILDER_AGENT | RUNNING   | 2025-08-05 14:35:31 | 2025-08-05 14:35:31 |
|  3 |           1 | BUDGET_MANAGER_AGENT    | RUNNING   | 2025-08-05 14:35:31 | 2025-08-05 14:35:31 |
|  4 |           2 | DATA_COLLECTOR_AGENT    | COMPLETED | 2025-08-05 14:38:36 | 2025-08-05 14:39:31 |
|  5 |           2 | ITINERARY_BUILDER_AGENT | COMPLETED | 2025-08-05 14:39:31 | 2025-08-05 14:39:52 |
|  6 |           2 | BUDGET_MANAGER_AGENT    | COMPLETED | 2025-08-05 14:39:31 | 2025-08-05 14:39:52 |
|  7 |           2 | REPORT_GENERATOR_AGENT  | COMPLETED | 2025-08-05 14:39:52 | 2025-08-05 14:40:22 |
+----+-------------+-------------------------+-----------+---------------------+---------------------+
```

```bash
mysql> select * from workflow;
+----+-----------+---------------------+---------------------+
| id | status    | created_at          | updated_at          |
+----+-----------+---------------------+---------------------+
|  1 | STARTED   | 2025-08-05 14:35:29 | 2025-08-05 14:35:29 |
|  2 | COMPLETED | 2025-08-05 14:38:36 | 2025-08-05 14:40:22 |
+----+-----------+---------------------+---------------------+
```

```bash
mysql> select * from workflow_agent_response;
+----+-------------+-------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+---------------------+
| id | workflow_id | workflow_agent_id | response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | created_at          | updated_at          |
+----+-------------+-------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+---------------------+
|  1 |           2 |                 4 | {"content": "{\"preferences\":{\"total_budget\":\"3000 USD\",\"preferred_route\":[\"Tokyo\",\"Kyoto\",\"Osaka\"],\"accommodation_type\":\"3-star hotel\",\"travel_dates\":{\"start_date\":\"2025-10-01\",\"end_date\":\"2025-10-05\"},\"special_interests\":[\"onsen\",\"local cuisine\",\"temple visits\"]},\"flights\":[{\"departure\":\"2025-10-01\",\"return\":\"2025-10-05\",\"from\":\"ICN\",\"to\":\"NRT\",\"price\":800},{\"departure\":\"2025-10-01\",\"return\":\"2025-10-05\",\"from\":\"ICN\",\"to\":\"KIX\",\"price\":750}],\"hotels\":[{\"city\":\"Tokyo\",\"name\":\"Tokyo Central 3-Star\",\"price_per_night\":150,\"total_stay_cost\":600},{\"city\":\"Kyoto\",\"name\":\"Kyoto Comfort Inn\",\"price_per_night\":120,\"total_stay_cost\":480},{\"city\":\"Osaka\",\"name\":\"Osaka Plaza Hotel\",\"price_per_night\":130,\"total_stay_cost\":520}],\"transport\":{\"JR_Pass_cost\":300,\"regional_transfers\":[{\"from\":\"Tokyo\",\"to\":\"Kyoto\",\"cost\":120},{\"from\":\"Kyoto\",\"to\":\"Osaka\",\"cost\":50}]},\"attractions\":[{\"city\":\"Tokyo\",\"attraction\":\"Senso-ji Temple\",\"hours\":\"6 AM - 5 PM\",\"public_holidays\":[\"2025-10-08\"],\"festivals\":[\"Tokyo Autumn Festival\"]},{\"city\":\"Kyoto\",\"attraction\":\"Kinkaku-ji\",\"hours\":\"9 AM - 5 PM\",\"public_holidays\":[\"2025-10-08\"],\"festivals\":[\"Kyoto Jidai Matsuri\"]},{\"city\":\"Osaka\",\"attraction\":\"Osaka Castle\",\"hours\":\"9 AM - 5 PM\",\"public_holidays\":[\"2025-10-08\"],\"festivals\":[\"Osaka Autumn Festival\"]}],\"weather\":[{\"city\":\"Tokyo\",\"forecast\":[\"20�C\",\"22�C\",\"18�C\",\"21�C\",\"19�C\"]},{\"city\":\"Kyoto\",\"forecast\":[\"19�C\",\"21�C\",\"17�C\",\"20�C\",\"18�C\"]},{\"city\":\"Osaka\",\"forecast\":[\"21�C\",\"23�C\",\"19�C\",\"22�C\",\"20�C\"]}]}", "filename": "itinerary_for_read.json"} | 2025-08-05 14:39:31 | 2025-08-05 14:39:31 |
|  2 |           2 |                 5 | {"content": "{\"day1\":{\"date\":\"2025-10-01\",\"city\":\"Tokyo\",\"morning\":{\"activity\":\"Visit Senso-ji Temple\",\"hours\":\"6 AM - 5 PM\",\"weather\":\"20�C/22�C\"},\"lunch\":{\"restaurant\":\"Asakusa Nanna Yoshihashi\",\"cuisine\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Explore Nakamise Street or nearby museums\",\"weather\":\"20�C/22�C\"},\"evening\":{\"transfer\":\"JR Pass to Kyoto for next day\",\"dinner\":\"Gyukatsu (Beef Cutlet) at Gyukatsu Kyoto Katsugyu\"}},\"day2\":{\"date\":\"2025-10-02\",\"city\":\"Kyoto\",\"morning\":{\"activity\":\"Visit Kinkaku-ji (Golden Pavilion)\",\"hours\":\"9 AM - 5 PM\",\"weather\":\"19�C/21�C\"},\"lunch\":{\"restaurant\":\"Nishiki Market\",\"cuisine\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Visit nearby temples or relax in an onsen if the weather permits\",\"weather\":\"19�C/21�C\"},\"evening\":{\"transfer\":\"Regional transfer to Osaka\",\"dinner\":\"Kaiseki Ryori (Traditional Meal) at Kikunoi\"}},\"day3\":{\"date\":\"2025-10-03\",\"city\":\"Osaka\",\"morning\":{\"activity\":\"Visit Osaka Castle\",\"hours\":\"9 AM - 5 PM\",\"weather\":\"21�C/23�C\"},\"lunch\":{\"restaurant\":\"Dotonbori Kushikatsu\",\"cuisine\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Walk along Dotonbori and try street food\",\"weather\":\"21�C/23�C\"},\"evening\":{\"transfer\":\"Free evening in Osaka\",\"dinner\":\"Okonomiyaki at Chibo\"}},\"day4\":{\"date\":\"2025-10-04\",\"city\":\"Osaka\",\"morning\":{\"activity\":\"Visit Shitenno-ji Temple\",\"hours\":\"8:30 AM - 4:30 PM\",\"weather\":\"19�C/20�C\"},\"lunch\":{\"restaurant\":\"Kuromon Ichiba Market\",\"cuisine\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Relax at Spa World or an onsen nearby\",\"weather\":\"19�C/20�C\"},\"evening\":{\"transfer\":\"Prepare for return to Tokyo\",\"dinner\":\"Takoyaki at Takoyaki Wanaka\"}},\"day5\":{\"date\":\"2025-10-05\",\"city\":\"Tokyo\",\"morning\":{\"activity\":\"Visit Ueno Park and Museums\",\"hours\":\"Public Parks Open All Day\",\"weather\":\"18�C/21�C\"},\"lunch\":{\"restaurant\":\"Ameyoko Street\",\"cuisine\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Explore Akihabara or relax before flight\",\"weather\":\"18�C/21�C\"},\"evening\":{\"transfer\":\"Flight to ICN\",\"dinner\":\"At airport (Tonkatsu set)\"}}}", "filename": "itinerary.json"} | 2025-08-05 14:39:52 | 2025-08-05 14:39:52 |
|  3 |           2 |                 6 | {"content": "{\"allocated\":{\"total_budget\":\"3000 USD\",\"flights\":800,\"accommodation\":1000,\"transport_non_JR\":200,\"meals\":600,\"entrance_fees\":400},\"spent\":{\"flights\":800,\"accommodation\":600,\"transport_non_JR\":170,\"meals\":600,\"entrance_fees\":400},\"remaining\":{\"total_remaining\":30},\"alternatives\":[\"Consider 2-star hotels for accommodation in each city to reduce costs, aiming for 100/night\",\"Utilize local bus services instead of taxis for regional transfers.\"]}", "filename": "budget.json"}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 2025-08-05 14:39:52 | 2025-08-05 14:39:52 |
|  4 |           2 |                 7 | {"content": "# Trip Report: Japan Itinerary and Budget Overview\n\n## Trip Overview\n- **Travel Dates:** 2025-10-01 to 2025-10-05  \n- **Route:** Tokyo -> Kyoto -> Osaka -> Tokyo  \n- **Total Budget:** 3000 USD  \n\n## Day-by-Day Itinerary\n### Day 1: Tokyo (2025-10-01)  \n- **Morning:**  \n  - **Activity:** Visit Senso-ji Temple  \n  - **Hours:** 6 AM - 5 PM  \n  - **Weather:** 20�C/22�C  \n- **Lunch:**  \n  - **Restaurant:** Asakusa Nanna Yoshihashi  \n  - **Cuisine:** Local Cuisine  \n- **Afternoon:**  \n  - **Activity:** Explore Nakamise Street or nearby museums  \n  - **Weather:** 20�C/22�C  \n- **Evening:**  \n  - **Transfer:** JR Pass to Kyoto for next day  \n  - **Dinner:** Gyukatsu (Beef Cutlet) at Gyukatsu Kyoto Katsugyu  \n\n### Day 2: Kyoto (2025-10-02)  \n- **Morning:**  \n  - **Activity:** Visit Kinkaku-ji (Golden Pavilion)  \n  - **Hours:** 9 AM - 5 PM  \n  - **Weather:** 19�C/21�C  \n- **Lunch:**  \n  - **Restaurant:** Nishiki Market  \n  - **Cuisine:** Local Cuisine  \n- **Afternoon:**  \n  - **Activity:** Visit nearby temples or relax in an onsen if the weather permits  \n  - **Weather:** 19�C/21�C  \n- **Evening:**  \n  - **Transfer:** Regional transfer to Osaka  \n  - **Dinner:** Kaiseki Ryori (Traditional Meal) at Kikunoi  \n\n### Day 3: Osaka (2025-10-03)  \n- **Morning:**  \n  - **Activity:** Visit Osaka Castle  \n  - **Hours:** 9 AM - 5 PM  \n  - **Weather:** 21�C/23�C  \n- **Lunch:**  \n  - **Restaurant:** Dotonbori Kushikatsu  \n  - **Cuisine:** Local Cuisine  \n- **Afternoon:**  \n  - **Activity:** Walk along Dotonbori and try street food  \n  - **Weather:** 21�C/23�C  \n- **Evening:**  \n  - **Transfer:** Free evening in Osaka  \n  - **Dinner:** Okonomiyaki at Chibo  \n\n### Day 4: Osaka (2025-10-04)  \n- **Morning:**  \n  - **Activity:** Visit Shitenno-ji Temple  \n  - **Hours:** 8:30 AM - 4:30 PM  \n  - **Weather:** 19�C/20�C  \n- **Lunch:**  \n  - **Restaurant:** Kuromon Ichiba Market  \n  - **Cuisine:** Local Cuisine  \n- **Afternoon:**  \n  - **Activity:** Relax at Spa World or an onsen nearby  \n  - **Weather:** 19�C/20�C  \n- **Evening:**  \n  - **Transfer:** Prepare for return to Tokyo  \n  - **Dinner:** Takoyaki at Takoyaki Wanaka  \n\n### Day 5: Tokyo (2025-10-05)  \n- **Morning:**  \n  - **Activity:** Visit Ueno Park and Museums  \n  - **Hours:** Public Parks Open All Day  \n  - **Weather:** 18�C/21�C  \n- **Lunch:**  \n  - **Restaurant:** Ameyoko Street  \n  - **Cuisine:** Local Cuisine  \n- **Afternoon:**  \n  - **Activity:** Explore Akihabara or relax before flight  \n  - **Weather:** 18�C/21�C  \n- **Evening:**  \n  - **Transfer:** Flight to ICN  \n  - **Dinner:** At airport (Tonkatsu set)  \n\n## Budget Summary\n| Category             | Allocated | Spent | Remaining |  \n|----------------------|-----------|-------|-----------|  \n| Flights              | 800 USD   | 800 USD | 0 USD  |  \n| Accommodation        | 1000 USD  | 600 USD | 400 USD  |  \n| Transport (non-JR)   | 200 USD   | 170 USD | 30 USD  |  \n| Meals                | 600 USD   | 600 USD | 0 USD  |  \n| Entrance Fees        | 400 USD   | 400 USD | 0 USD  |  \n| **Total**            | **3000 USD** | **2840 USD** | **30 USD** |  \n\n## Reservation Checklist\n- Flight Number: [Insert Flight Number]  \n- Hotel Names: [List of Hotels]  \n- JR Pass: Confirmed  \n\n## Packing & Pre-departure Reminders\n- **Travel Documents:** Passport, itinerary, travel insurance  \n- **Packing Tips:** Pack layered clothing due to varying temperatures  \n- **Electronics:** Ensure to bring a power adapter for Japan  \n\n## Cost-saving Tips\n- Consider 2-star hotels for accommodation in each city to reduce costs, aiming for 100/night  \n- Utilize local bus services instead of taxis for regional transfers.  \n\n## Must-see Spots\n- Tokyo: Senso-ji Temple, Nakamise Street  \n- Kyoto: Kinkaku-ji, Nishiki Market  \n- Osaka: Osaka Castle, Dotonbori  \n\n## Onsen & Temple Visit Recommendations\n- Onsen: Spa World in Osaka  \n- Temples: Shitenno-ji Temple, Kinkaku-ji  \n", "filename": "report.md"} | 2025-08-05 14:40:22 | 2025-08-05 14:40:22 |
+----+-------------+-------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+---------------------+
4 rows in set (0.00 sec)
```

`ws://127.0.0.1:8000/ws/{workflow_id}`

- WebSocket API

### 웹소캣 실행 결과

**성공**

<img width="1481" height="790" alt="image" src="https://github.com/user-attachments/assets/42f6fba6-094f-4f0d-bf2c-ac74f4763346" />


**실패**

<img width="1511" height="258" alt="image" src="https://github.com/user-attachments/assets/17695482-9d43-46ac-96c9-217cca5c529c" />


### workflow 상태

```json
{
    "workflow_status": {
        "status": "RUNNING",
        "start_at": "2025-08-06T04:37:12",
        "updated_at": "2025-08-06T04:37:12"
    },
    "agent_responses": []
}
```

```json
{
    "status": "COMPLETED",
    "timestamp": "2025-08-06T04:37:59.973164"
}
```

### 에이전트 상태

```json
{
    "agent_name": "BUDGET_MANAGER_AGENT",
    "status": "RUNNING",
    "timestamp": "2025-08-06T04:37:30.837986"
}
```

```json
{
    "agent_name": "BUDGET_MANAGER_AGENT",
    "status": "COMPLETED",
    "timestamp": "2025-08-06T04:37:34.865622"
}
```

### 에이전트 응답

```json
{
    "agent_name": "ITINERARY_BUILDER_AGENT",
    "response_data": {
        "filename": "itinerary_2.json",
        "content": "{\"day1\":{\"city\":\"Tokyo\",\"date\":\"2025-10-01\",\"morning\":{\"activity\":\"Visit Senso-ji Temple\",\"hours\":\"6:00 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Asakusa Imahan - Local Cuisine (Sukiyaki)\",\"type\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Sightseeing around Asakusa & Nakamise Street\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Plan for next day to Kyoto\",\"dinner\":{\"location\":\"Uobei Sushi - Local Cuisine\",\"type\":\"Sushi\"}}},\"day2\":{\"city\":\"Tokyo\",\"date\":\"2025-10-02\",\"morning\":{\"activity\":\"Visit Tokyo National Museum\",\"hours\":\"9:30 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Ueno Park - Local Cuisine (Street Food)\",\"type\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Indoor: Explore Ueno Zoo (Rainy Weather)\",\"weather\":\"Rain\"},\"evening\":{\"transfer\":\"Plan for next day to Kyoto\",\"dinner\":{\"location\":\"Matsuya - Local Cuisine (Gyudon)\",\"type\":\"Gyudon\"}}},\"day3\":{\"city\":\"Kyoto\",\"date\":\"2025-10-03\",\"morning\":{\"activity\":\"Visit Kinkaku-ji (The Golden Pavilion)\",\"hours\":\"9:00 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Shishin Samurai Restaurant - Local Cuisine\",\"type\":\"Kaiseki\"},\"afternoon\":{\"activity\":\"Relax at Kyoto Onsen\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Prepare for next day to Osaka\",\"dinner\":{\"location\":\"Gion Nanba - Local Cuisine (Yudofu)\",\"type\":\"Yudofu\"}}},\"day4\":{\"city\":\"Kyoto\",\"date\":\"2025-10-04\",\"morning\":{\"activity\":\"Visit Fushimi Inari-taisha Shrine\",\"hours\":\"24 Hours Open\"},\"lunch\":{\"location\":\"Inari Sushi Kappo - Local Cuisine\",\"type\":\"Sushi\"},\"afternoon\":{\"activity\":\"Explore Nijo Castle\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Stay in Osaka for next day activities\",\"dinner\":{\"location\":\"Kushikatsu Daruma - Local Cuisine (Kushikatsu)\",\"type\":\"Kushikatsu\"}}},\"day5\":{\"city\":\"Osaka\",\"date\":\"2025-10-05\",\"morning\":{\"activity\":\"Visit Osaka Castle\",\"hours\":\"9:00 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Dotonbori - Local Cuisine (Takoyaki)\",\"type\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Shopping in Shinsaibashi\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Prepare for your flight back\",\"dinner\":{\"location\":\"Izakaya - Local Cuisine (Various)\",\"type\":\"Japanese Pub Fare\"}}}}"
    },
    "timestamp": "2025-08-06T04:37:45.204325"
}
```

### workflow 실행 완료 후 socket 응답

```json
{
    "workflow_status": {
        "status": "COMPLETED",
        "start_at": "2025-08-06T04:37:12",
        "updated_at": "2025-08-06T04:38:00"
    },
    "agent_responses": [
        {
            "response": {
                "content": "{\"preferences\": {\"total_budget\": \"3000 USD\",\"preferred_route\": [\"Tokyo\", \"Kyoto\", \"Osaka\"],\"accommodation_type\": \"3-star hotel\",\"travel_dates\": {\"start_date\": \"2025-10-01\",\"end_date\": \"2025-10-05\"},\"special_interests\": [\"onsen\", \"local cuisine\", \"temple visits\"]},\"flights\": [{\"origin\": \"ICN\",\"destination\": \"NRT\",\"departure\": \"2025-09-30\",\"return\": \"2025-10-06\",\"cost\": \"xxx USD\"}],\"hotels\": [{\"city\": \"Tokyo\",\"name\": \"Tokyo 3-Star Hotel\",\"check_in\": \"2025-10-01\",\"check_out\": \"2025-10-03\",\"cost_per_night\": \"xxx USD\"},{\"city\": \"Kyoto\",\"name\": \"Kyoto 3-Star Hotel\",\"check_in\": \"2025-10-03\",\"check_out\": \"2025-10-05\",\"cost_per_night\": \"xxx USD\"}],\"transport\": {\"JR_Pass_cost\": \"xxx USD\",\"regional_transfers\": [\"Tokyo to Kyoto\", \"Kyoto to Osaka\"]},\"attractions\": [{\"city\": \"Tokyo\",\"attraction\": \"Senso-ji Temple\",\"hours\": \"6:00 AM - 5:00 PM\",\"public_holidays\": [],\"festivals\": [\"Tokyo Autumn Festival\"]}],\"weather\": [{\"city\": \"Tokyo\",\"forecast\": [{\"date\": \"2025-10-01\",\"weather\": \"Sunny\",\"temperature\": \"23°C\"},{\"date\": \"2025-10-02\",\"weather\": \"Rain\",\"temperature\": \"20°C\"}]}]}",
                "filename": "itinerary_for_read_2.json"
            },
            "start_at": "2025-08-06T04:37:31",
            "updated_at": "2025-08-06T04:37:31"
        },
        {
            "response": {
                "content": "{\"allocated\":{\"flights\":800,\"accommodation\":1000,\"transport\":200,\"meals\":600,\"entrance fees\":400},\"spent\":{\"flights\":800,\"accommodation\":\"xxx USD\",\"transport\":\"xxx USD\",\"meals\":600,\"entrance fees\":400},\"remaining\":{\"flights\":0,\"accommodation\":\"1000 - xxx USD\",\"transport\":\"200 - xxx USD\",\"meals\":0,\"entrance fees\":0},\"alternatives\":[\"consider 2-star hotels for accommodation savings\",\"use local buses instead of taxis for transport savings\"]}",
                "filename": "budget_2.json"
            },
            "start_at": "2025-08-06T04:37:35",
            "updated_at": "2025-08-06T04:37:35"
        },
        {
            "response": {
                "content": "{\"day1\":{\"city\":\"Tokyo\",\"date\":\"2025-10-01\",\"morning\":{\"activity\":\"Visit Senso-ji Temple\",\"hours\":\"6:00 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Asakusa Imahan - Local Cuisine (Sukiyaki)\",\"type\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Sightseeing around Asakusa & Nakamise Street\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Plan for next day to Kyoto\",\"dinner\":{\"location\":\"Uobei Sushi - Local Cuisine\",\"type\":\"Sushi\"}}},\"day2\":{\"city\":\"Tokyo\",\"date\":\"2025-10-02\",\"morning\":{\"activity\":\"Visit Tokyo National Museum\",\"hours\":\"9:30 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Ueno Park - Local Cuisine (Street Food)\",\"type\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Indoor: Explore Ueno Zoo (Rainy Weather)\",\"weather\":\"Rain\"},\"evening\":{\"transfer\":\"Plan for next day to Kyoto\",\"dinner\":{\"location\":\"Matsuya - Local Cuisine (Gyudon)\",\"type\":\"Gyudon\"}}},\"day3\":{\"city\":\"Kyoto\",\"date\":\"2025-10-03\",\"morning\":{\"activity\":\"Visit Kinkaku-ji (The Golden Pavilion)\",\"hours\":\"9:00 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Shishin Samurai Restaurant - Local Cuisine\",\"type\":\"Kaiseki\"},\"afternoon\":{\"activity\":\"Relax at Kyoto Onsen\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Prepare for next day to Osaka\",\"dinner\":{\"location\":\"Gion Nanba - Local Cuisine (Yudofu)\",\"type\":\"Yudofu\"}}},\"day4\":{\"city\":\"Kyoto\",\"date\":\"2025-10-04\",\"morning\":{\"activity\":\"Visit Fushimi Inari-taisha Shrine\",\"hours\":\"24 Hours Open\"},\"lunch\":{\"location\":\"Inari Sushi Kappo - Local Cuisine\",\"type\":\"Sushi\"},\"afternoon\":{\"activity\":\"Explore Nijo Castle\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Stay in Osaka for next day activities\",\"dinner\":{\"location\":\"Kushikatsu Daruma - Local Cuisine (Kushikatsu)\",\"type\":\"Kushikatsu\"}}},\"day5\":{\"city\":\"Osaka\",\"date\":\"2025-10-05\",\"morning\":{\"activity\":\"Visit Osaka Castle\",\"hours\":\"9:00 AM - 5:00 PM\"},\"lunch\":{\"location\":\"Dotonbori - Local Cuisine (Takoyaki)\",\"type\":\"Local Cuisine\"},\"afternoon\":{\"activity\":\"Shopping in Shinsaibashi\",\"weather\":\"Sunny\"},\"evening\":{\"transfer\":\"Prepare for your flight back\",\"dinner\":{\"location\":\"Izakaya - Local Cuisine (Various)\",\"type\":\"Japanese Pub Fare\"}}}}",
                "filename": "itinerary_2.json"
            },
            "start_at": "2025-08-06T04:37:45",
            "updated_at": "2025-08-06T04:37:45"
        },
        {
            "response": {
                "content": "# Trip Overview\n**Date:** 2025-10-01 to 2025-10-05  \n**Route:** Tokyo -> Kyoto -> Osaka  \n**Total Budget:** 3000 USD  \n\n---\n\n# Day-by-Day Itinerary\n## Day 1: Tokyo (2025-10-01)  \n- **Morning:** Visit Senso-ji Temple (6:00 AM - 5:00 PM)  \n- **Lunch:** Asakusa Imahan - Local Cuisine (Sukiyaki)  \n- **Afternoon:** Sightseeing around Asakusa & Nakamise Street (Weather: Sunny)  \n- **Evening:**  \n  - Transfer: Plan for next day to Kyoto  \n  - Dinner: Uobei Sushi - Local Cuisine  \n\n---  \n\n## Day 2: Tokyo (2025-10-02)  \n- **Morning:** Visit Tokyo National Museum (9:30 AM - 5:00 PM)  \n- **Lunch:** Ueno Park - Local Cuisine (Street Food)  \n- **Afternoon:** Indoor: Explore Ueno Zoo (Weather: Rain)  \n- **Evening:**  \n  - Transfer: Plan for next day to Kyoto  \n  - Dinner: Matsuya - Local Cuisine (Gyudon)  \n\n---  \n\n## Day 3: Kyoto (2025-10-03)  \n- **Morning:** Visit Kinkaku-ji (The Golden Pavilion) (9:00 AM - 5:00 PM)  \n- **Lunch:** Shishin Samurai Restaurant - Local Cuisine (Kaiseki)  \n- **Afternoon:** Relax at Kyoto Onsen (Weather: Sunny)  \n- **Evening:**  \n  - Transfer: Prepare for next day to Osaka  \n  - Dinner: Gion Nanba - Local Cuisine (Yudofu)  \n\n---  \n\n## Day 4: Kyoto (2025-10-04)  \n- **Morning:** Visit Fushimi Inari-taisha Shrine (24 Hours Open)  \n- **Lunch:** Inari Sushi Kappo - Local Cuisine (Sushi)  \n- **Afternoon:** Explore Nijo Castle (Weather: Sunny)  \n- **Evening:**  \n  - Transfer: Stay in Osaka for next day activities  \n  - Dinner: Kushikatsu Daruma - Local Cuisine (Kushikatsu)  \n\n---  \n\n## Day 5: Osaka (2025-10-05)  \n- **Morning:** Visit Osaka Castle (9:00 AM - 5:00 PM)  \n- **Lunch:** Dotonbori - Local Cuisine (Takoyaki)  \n- **Afternoon:** Shopping in Shinsaibashi (Weather: Sunny)  \n- **Evening:**  \n  - Transfer: Prepare for your flight back  \n  - Dinner: Izakaya - Local Cuisine (Various)  \n\n---  \n\n# Budget Summary Table  \n| Category        | Allocated | Spent          | Remaining               |  \n|----------------|-----------|----------------|-------------------------|  \n| Flights        | 800 USD   | 800 USD        | 0 USD                   |  \n| Accommodation  | 1000 USD  | xxx USD        | 1000 - xxx USD          |  \n| Transport      | 200 USD   | xxx USD        | 200 - xxx USD           |  \n| Meals          | 600 USD   | 600 USD        | 0 USD                   |  \n| Entrance Fees  | 400 USD   | 400 USD        | 0 USD                   |  \n\n---  \n\n# Reservation Checklist  \n- Flight #  \n- Hotel Names  \n- JR Pass  \n\n---  \n\n# Packing & Pre-departure Reminders  \n- **Cost-saving tips:**  \n  - Consider 2-star hotels for accommodation savings  \n  - Use local buses instead of taxis for transport savings  \n\n- **Must-see spots:**  \n  - Senso-ji Temple, Kinkaku-ji, Fushimi Inari-taisha Shrine  \n\n- **Onsen & temple visit recommendations:**  \n  - Kyoto Onsen recommended for a relaxing experience.",
                "filename": "report_2.md"
            },
            "start_at": "2025-08-06T04:38:00",
            "updated_at": "2025-08-06T04:38:00"
        }
    ]
}
```

## Database

<img width="598" height="710" alt="image" src="https://github.com/user-attachments/assets/7ea21ca5-5444-4d41-91b4-7816b6df9920" />


### workflow

```
+------------+------------------------------------------------+------+-----+---------+----------------+
| Field      | Type                                           | Null | Key | Default | Extra          |
+------------+------------------------------------------------+------+-----+---------+----------------+
| id         | int                                            | NO   | PRI | NULL    | auto_increment |
| status     | enum('STARTED','RUNNING','COMPLETED','FAILED') | NO   | MUL | NULL    |                |
| created_at | datetime                                       | YES  |     | NULL    |                |
| updated_at | datetime                                       | YES  |     | NULL    |                |
+------------+------------------------------------------------+------+-----+---------+----------------+
```

### workflow_agent

```
+-------------+------------------------------------------------+------+-----+---------+----------------+
| Field       | Type                                           | Null | Key | Default | Extra          |
+-------------+------------------------------------------------+------+-----+---------+----------------+
| id          | int                                            | NO   | PRI | NULL    | auto_increment |
| workflow_id | int                                            | NO   | MUL | NULL    |                |
| agent_name  | varchar(100)                                   | NO   | MUL | NULL    |                |
| status      | enum('STARTED','RUNNING','COMPLETED','FAILED') | NO   | MUL | NULL    |                |
| created_at  | datetime                                       | YES  |     | NULL    |                |
| updated_at  | datetime                                       | YES  |     | NULL    |                |
+-------------+------------------------------------------------+------+-----+---------+----------------+
```

### workflow_agent_response

```
+-------------------+----------+------+-----+---------+----------------+
| Field             | Type     | Null | Key | Default | Extra          |
+-------------------+----------+------+-----+---------+----------------+
| id                | int      | NO   | PRI | NULL    | auto_increment |
| workflow_id       | int      | NO   | MUL | NULL    |                |
| workflow_agent_id | int      | NO   | MUL | NULL    |                |
| response          | json     | YES  |     | NULL    |                |
| created_at        | datetime | YES  |     | NULL    |                |
| updated_at        | datetime | YES  |     | NULL    |                |
+-------------------+----------+------+-----+---------+----------------+
```
