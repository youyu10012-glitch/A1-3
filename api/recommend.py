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

        travel_style = body.get('style', '힐링/자연')
        schedule = body.get('schedule', '당일치기')
        companion = body.get('companion', '나홀로')

        gemini_key = os.getenv("GEMINI_API_KEY")

        if gemini_key:
            try:
                from google import genai
                client = genai.Client(api_key=gemini_key)
                prompt = (
                    f"여행 스타일: {travel_style}, 일정: {schedule}, 동행: {companion}. "
                    "대한민국 국내 여행지 1곳을 추천하고 이유와 팁을 3줄로 한국어로 작성해줘."
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                ai_text = response.text
            except Exception as e:
                ai_text = f"API 호출 오류 (목업 데이터): {travel_style} 맞춤 추천 지역은 '강릉 안목해변'입니다."
        else:
            ai_text = f"[테스트 모드] {travel_style} 취향에 맞는 추천 지역은 '강릉 안목해변'입니다. 바다를 보며 힐링하기 좋습니다."

        response_payload = {
            "status": "success",
            "result": ai_text
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode('utf-8'))