document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("recommend-form");
  const submitBtn = document.getElementById("submit-btn");
  const btnText = document.getElementById("btn-text");
  const statusMsg = document.getElementById("status-message");
  const resultBox = document.getElementById("result-box");
  const resultText = document.getElementById("result-text");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const style = document.getElementById("style").value.trim();
    const schedule = document.getElementById("schedule").value.trim();
    const companion = document.getElementById("companion").value.trim();

    if (!style || !schedule || !companion) {
      statusMsg.textContent = "모든 항목을 입력해 주세요.";
      return;
    }

    // 로딩 UI 시작
    submitBtn.disabled = true;
    btnText.textContent = "AI 여행지 분석 중...";
    statusMsg.textContent = "취향에 맞는 최적의 여행지를 탐색 중입니다...";
    resultBox.style.display = "none";

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ style, schedule, companion })
      });

      if (!response.ok) {
        throw new Error(`서버 응답 오류 (상태 코드: ${response.status})`);
      }

      const data = await response.json();
      
      statusMsg.textContent = "";
      resultBox.style.display = "block";
      resultText.textContent = data.result || "추천 결과를 가져오지 못했습니다.";
      
      // 결과 영역으로 스크롤 이동
      resultBox.scrollIntoView({ behavior: "smooth", block: "nearest" });

    } catch (err) {
      console.error("추천 요청 실패:", err);
      statusMsg.textContent = "추천 요청 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.";
    } finally {
      submitBtn.disabled = false;
      btnText.textContent = "여행지 추천 받기";
    }
  });
});
