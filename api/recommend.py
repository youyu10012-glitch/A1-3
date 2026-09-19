import json
import os
from http.server import BaseHTTPRequestHandler

MOCK_RECOMMENDATION = {
    "title": "강릉, 파도와 커피 사이의 느린 주말",
    "location": "강원 강릉 / 안목해변 · 초당동",
    "description": "아침에는 바다를 따라 천천히 걷고, 오후에는 초당동의 작은 카페에 머물러 보세요. 계획을 비워둘수록 장면이 풍성해지는 여행입니다.",
    "reason": "입력한 취향을 바탕으로 이동 부담이 적고, 동행자와 대화할 여백이 있는 여행지를 골랐어요.",
    "best_time": "추천 시기: 봄, 초가을",
    "tip": "TIP: 일몰 30분 전 안목해변 산책"
}


def mock_response(style, schedule, companions):
    recommendation = dict(MOCK_RECOMMENDATION)
    recommendation["reason"] = f"'{style}' 취향과 {schedule} 일정, {companions} 여행에 맞춰 느긋한 바다의 리듬을 골랐어요."
    return recommendation


def generate_with_gemini(style, schedule, companions):
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = f"""당신은 국내 여행 큐레이터 TripWhisper입니다.
사용자의 여행 정보를 바탕으로 국내 여행지 한 곳을 추천하세요.
여행 스타일: {style}
일정: {schedule}
동행자: {companions}
반드시 아래 JSON 형식만 반환하세요. 마크다운 코드블록은 사용하지 마세요.
{{"title":"짧고 감각적인 제목", "location":"지역과 핵심 장소", "description":"2~3문장의 구체적인 여행 장면", "reason":"입력과 추천이 연결되는 이유", "best_time":"추천 시기", "tip":"실용적인 작은 팁"}}"""
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    raw_text = (response.text or "").strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").replace("json", "", 1).strip()
    return json.loads(raw_text)


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(204, {})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            style = str(data.get("style", "")).strip()
            schedule = str(data.get("schedule", "")).strip()
            companions = str(data.get("companions", "")).strip()
            if not all((style, schedule, companions)):
                self._send_json(400, {"error": "여행 스타일, 일정, 동행자를 모두 입력해 주세요."})
                return

            if os.environ.get("GEMINI_API_KEY"):
                try:
                    recommendation = generate_with_gemini(style, schedule, companions)
                except Exception:
                    recommendation = mock_response(style, schedule, companions)
            else:
                recommendation = mock_response(style, schedule, companions)
            self._send_json(200, {"recommendation": recommendation, "source": "gemini" if os.environ.get("GEMINI_API_KEY") else "mock"})
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "요청 형식을 확인해 주세요."})
        except Exception:
            self._send_json(500, {"error": "추천을 준비하지 못했어요. 잠시 후 다시 시도해 주세요."})

    def do_GET(self):
        self._send_json(405, {"error": "POST 요청만 지원합니다."})
