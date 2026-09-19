# TripWhisper

취향과 일정, 동행자를 바탕으로 국내 여행지 한 곳을 큐레이션하는 AI 웹 서비스입니다. 검색 결과를 길게 나열하는 대신, 사용자가 실제로 상상하고 실행할 수 있는 여행 장면과 작은 팁을 제공합니다.

## 주요 기능

- Hero, 서비스 소개, AI 추천기, FAQ로 구성된 단일 페이지 네비게이션
- 여행 스타일·일정·동행자를 입력하는 반응형 추천 폼
- `/api/recommend`를 통한 Gemini AI 추천
- API 키가 없거나 외부 AI 호출이 실패해도 동작하는 목업 fallback
- 빈 입력, API 오류, 10초 초과 지연에 대한 사용자 안내
- 모바일·태블릿·데스크톱 대응 UI

## 기술 스택

- Frontend: 순수 HTML, CSS, Vanilla JavaScript
- Backend: Vercel Serverless Functions, Python `BaseHTTPRequestHandler`
- AI: Google Gemini via `google-genai`
- Hosting: Vercel

## 프로젝트 구조

```text
.
├── index.html
├── css/style.css
├── js/app.js
├── api/recommend.py
├── PLAN.md
├── requirements.txt
└── vercel.json
```

## 로컬 실행

정적 프론트엔드는 별도 빌드가 필요 없습니다. Python이 설치된 환경에서 프로젝트 루트로 이동해 실행하세요.

```bash
python3 -m http.server 8000
```

그 다음 브라우저에서 `http://localhost:8000`을 엽니다. 위 방식은 정적 화면 확인용이며, `/api/recommend` 서버리스 함수는 Vercel 런타임에서 실행됩니다.

로컬에서 API까지 함께 테스트하려면 Vercel CLI를 사용합니다.

```bash
npm install -g vercel
vercel dev
```

## 환경 변수

Gemini를 실제로 호출하려면 Vercel 프로젝트의 Environment Variables에 다음 값을 등록하세요. API 키는 소스 코드, README, 커밋에 직접 작성하지 않습니다.

```text
GEMINI_API_KEY=your_gemini_api_key
```

키를 설정하지 않은 로컬 환경에서도 `/api/recommend`는 강릉 기반 목업 응답을 반환하므로 입력·로딩·결과 표시 UX를 테스트할 수 있습니다.

## Vercel 배포

1. 이 저장소를 GitHub에 push합니다.
2. Vercel에서 `Add New Project`를 선택하고 GitHub 저장소를 연결합니다.
3. Framework Preset은 `Other` 또는 자동 감지를 사용합니다. 별도 Build Command는 필요하지 않습니다.
4. Project Settings → Environment Variables에 `GEMINI_API_KEY`를 등록합니다.
5. Deploy를 실행하고 발급된 URL에서 네비게이션, 반응형 화면, AI 추천을 확인합니다.

Vercel CLI를 사용하면 다음처럼 배포할 수 있습니다.

```bash
vercel
vercel --prod
```

배포 후 URL은 제출 시 아래처럼 기록합니다.

```text
배포 URL: https://your-project.vercel.app
```

## 테스트 체크리스트

- 정상 입력: `느린 산책과 로컬 카페` / `2박 3일` / `연인`
- 빈 입력: `필수값을 입력하세요` 안내 표시
- 목업 API: `GEMINI_API_KEY` 없이도 추천 결과 표시
- 모바일: 390px 폭에서 폼과 결과 패널 가로 넘침 없음
- 데스크톱: 1280px 폭에서 Hero 이미지와 텍스트가 겹치지 않음
- 오류 및 지연: API 오류 메시지와 10초 타임아웃 안내 표시

서비스 기획과 AI 입출력·실패 처리 기준은 [PLAN.md](PLAN.md)에 정리했습니다.
