import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}

        travel_style = body.get('style', '힐링, 감성 카페, 산책')
        schedule = body.get('schedule', '1박 2일')
        companion = body.get('companion', '혼자')

        gemini_key = os.getenv("GEMINI_API_KEY")
        curation_data = None

        if gemini_key:
            try:
                from google import genai
                from google.genai import types
                
                client = genai.Client(api_key=gemini_key)
                prompt = f"""
당신은 대한민국 최고 수준의 프리미엄 감성 여행 에디터입니다.
아래 여행자의 조건을 바탕으로 깊이 있고 감각적인 국내 맞춤 여행 일정을 추천하세요.

[여행자 프로필]
- 여행 스타일: {travel_style}
- 일정: {schedule}
- 동행자: {companion}

반드시 아래 JSON 포맷으로만 응답하세요:
{{
  "destination": "여행지 이름 (예: 강원도 고성)",
  "tagline": "감성적인 한 줄 슬로건",
  "reason": "이 여행자를 위해 이곳을 선정한 이유 (2~3문장)",
  "highlights": [
    {{"title": "스팟/장소 1", "desc": "설명 및 추천 이유"}},
    {{"title": "스팟/장소 2", "desc": "설명 및 추천 이유"}},
    {{"title": "스팟/장소 3", "desc": "설명 및 추천 이유"}}
  ],
  "itinerary": [
    {{"time": "Day 1 오전/오후", "activity": "일정 및 동선 내용"}},
    {{"time": "Day 2 또는 저녁", "activity": "일정 및 동선 내용"}}
  ],
  "curatorTip": "현지 로컬 맛집이나 최적의 방문 팁 (2문장)",
  "kakaoQuery": "카카오맵 검색용 키워드 (예: 고성 오션뷰 카페)"
}}
"""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                curation_data = json.loads(response.text)
            except Exception as e:
                curation_data = None

        # fallback 풍부한 예시 데이터 (API 키 오류나 딜레이 방지용)
        if not curation_data:
            curation_data = {
                "destination": "강원도 고성 & 속초",
                "tagline": "인파를 벗어나 푸른 파도와 담백한 숲길을 걷는 시간",
                "reason": f"복잡한 일상에서 벗어나 '{travel_style}'을 온전히 누릴 수 있는 최적의 동선입니다. {schedule} 동안 {companion}과 함께 고요한 해변도로를 달리며 리프레시하기에 제격입니다.",
                "highlights": [
                    {"title": "송지호 둘레길 & 해변", "desc": "호수와 솔숲길, 에메랄드빛 바다가 맞닿아 있어 산책하기 가장 평화로운 명소입니다."},
                    {"title": "아야진 해변 감성 카페거리", "desc": "알록달록한 방파제길을 따라 바다를 바라보며 로컬 드립 커피를 즐길 수 있습니다."},
                    {"title": "화암사 숲길 & 수바위", "desc": "울산바위가 한눈에 들어오는 비밀스러운 사찰 숲길로 여유로운 치유의 시간을 선사합니다."}
                ],
                "itinerary": [
                    {"time": "Day 1", "activity": "오후 송지호 솔숲 산책 ➔ 아야진 해변 카페 투어 ➔ 로컬 해산물 요리"},
                    {"time": "Day 2", "activity": "화암사 숲길 가벼운 트레킹 ➔ 영랑호 호수길 드라이브 ➔ 귀가"}
                ],
                "curatorTip": "주말 오후보다는 오전 10시 전후에 해변 산책로를 걸으면 한적한 바다를 오롯이 누릴 수 있습니다.",
                "kakaoQuery": "고성 아야진 해변"
            }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(curation_data, ensure_ascii=False).encode('utf-8'))
