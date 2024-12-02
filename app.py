# streamlit run app.py
import streamlit as st
from openai import OpenAI

api_key = "sk-"
client = OpenAI(api_key=api_key)

st.session_state['api_key'] = api_key
if 'openai_client' in st.session_state:
    client = st.session_state['openai_client']
else:
    client = OpenAI(api_key=api_key)
    st.session_state['openai_client'] = client



st.header("부산 종합 현지인 가이드 챗봇")

col1, col2, col3, col4, col5 = st.columns(5)
with col5:
    if st.button("Clear"):
        st.session_state.messages = []
        del st.session_state.thread


# 부산 가이드 챗봇 데이터 변수 설정
city_info = {
    "name": "부산",
    "description": "대한민국 남동부에 위치한 해양 도시로, 아름다운 해변과 현대적 시설, 풍부한 문화유산을 갖추고 있다.",
    "language": "한국어",
    "currency": "원(₩)",
    "climate": {
        "summer": "덥고 습하며 해수욕장이 붐비는 시즌",
        "winter": "온화하지만 바람이 강함",
        "spring_fall": "여행하기 가장 좋은 계절"
    }
}

landmarks = {
    "historical": ["범어사", "동래읍성"],
    "natural": ["해운대 해수욕장", "감천문화마을", "태종대"],
    "modern": ["광안대교", "부산국제영화제 거리"],
    "local_experience": ["국제시장", "자갈치시장"]
}

food_and_restaurants = {
    "local_dishes": ["돼지국밥", "밀면", "씨앗호떡"],
    "recommended": [
        {"name": "할매국밥", "location": "남포동", "specialty": "돼지국밥"},
        {"name": "광안밀면", "location": "광안리", "specialty": "밀면"},
        {"name": "백화양곱창", "location": "서면", "specialty": "양곱창"}
    ]
}

activities = {
    "water": ["요트 투어", "수영강 카약"],
    "land": ["해운대 스카이 캡슐"]
}

transportation = {
    "within_city": ["지하철", "버스", "택시", "도보"],
    "to_other_cities": ["KTX", "고속버스"]
}

culture_and_etiquette = {
    "dialect": "부산 사투리 ('오이소, 보이소, 사이소!')",
    "tips": ["바다 근처는 항상 깨끗하게 이용", "전통시장에서는 흥정 가능"]
}

emergency_contacts = {
    "hospital": {"name": "부산대병원", "phone": "051-240-7000"},
    "police": {"name": "관광경찰센터", "phone": "051-899-4000"},
    "emergency_numbers": {"fire_and_medical": "119", "foreign_help": "1330"}
}

# 시스템 프롬프트
system_prompt = f"""
너는 부산을 기반으로 한 종합 현지인 가이드 챗봇이다. 
너의 역할은 관광객들에게 부산에 관한 정보를 제공하고, 여행 플랜을 맞춤 추천하며, 필요한 실시간 정보를 안내하는 것이다.

부산에 대한 주요 정보:
- 도시 이름: {city_info['name']}
- 소개: {city_info['description']}
- 언어: {city_info['language']}
- 화폐: {city_info['currency']}
- 날씨 정보:
  * 여름: {city_info['climate']['summer']}
  * 겨울: {city_info['climate']['winter']}
  * 봄/가을: {city_info['climate']['spring_fall']}

추천 명소:
- 역사적 명소: {", ".join(landmarks['historical'])}
- 자연경관: {", ".join(landmarks['natural'])}
- 현대적 명소: {", ".join(landmarks['modern'])}
- 로컬 체험: {", ".join(landmarks['local_experience'])}

부산 음식과 맛집:
- 지역 음식: {", ".join(food_and_restaurants['local_dishes'])}
- 추천 맛집:
  {", ".join([f"{r['name']} ({r['location']}, 대표 메뉴: {r['specialty']})" for r in food_and_restaurants['recommended']])}

교통 정보:
- 도시 내 이동수단: {", ".join(transportation['within_city'])}
- 다른 도시로 이동: {", ".join(transportation['to_other_cities'])}

문화와 에티켓:
- 부산 사투리: {culture_and_etiquette['dialect']}
- 에티켓 팁: {", ".join(culture_and_etiquette['tips'])}

비상 연락처:
- 병원: {emergency_contacts['hospital']['name']} ({emergency_contacts['hospital']['phone']})
- 경찰: {emergency_contacts['police']['name']} ({emergency_contacts['police']['phone']})
- 긴급 전화: 화재 및 응급 ({emergency_contacts['emergency_numbers']['fire_and_medical']}), 외국인 헬프라인 ({emergency_contacts['emergency_numbers']['foreign_help']})

질문에 따라 부산의 명소, 맛집, 교통수단 등 맞춤형 정보를 제공하고, 요청에 따라 실시간 정보를 안내하라. 친절하고 이해하기 쉬운 어조로 응답하라.
"""




def show_message(msg):
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])


client = st.session_state.get('openai_client', None)

if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = [
        {"role":"system","content": system_prompt}
    ]


for msg in st.session_state.chatbot_messages[1:]:
    show_message(msg)

if prompt := st.chat_input("What is up?"):
    msg = {"role":"user", "content":prompt}
    show_message(msg)
    st.session_state.chatbot_messages.append(msg)

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = st.session_state.chatbot_messages
    )
    msg = {"role":"assistant", "content":response.choices[0].message.content}
    show_message(msg)
    st.session_state.chatbot_messages.append(msg)