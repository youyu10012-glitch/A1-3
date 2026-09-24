document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("recommend-form");
  const submitBtn = document.getElementById("submit-btn");
  const btnText = document.getElementById("btn-text");
  const statusMsg = document.getElementById("status-message");
  const resultBox = document.getElementById("result-box");

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

    submitBtn.disabled = true;
    btnText.textContent = "✨ 큐레이션 리포트 생성 중...";
    statusMsg.textContent = "AI가 최적의 스팟과 일정을 선별하고 있습니다...";
    resultBox.style.display = "none";

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ style, schedule, companion })
      });

      if (!response.ok) throw new Error("서버 응답 오류");

      const data = await response.json();
      statusMsg.textContent = "";

      // 큐레이션 결과 HTML 템플릿 생성
      const highlightsHtml = (data.highlights || []).map((h, idx) => `
        <div class="highlight-item">
          <span class="spot-num">SPOT 0${idx + 1}</span>
          <div class="spot-info">
            <strong>${h.title}</strong>
            <p>${h.desc}</p>
          </div>
        </div>
      `).join("");

      const itineraryHtml = (data.itinerary || []).map(item => `
        <div class="itinerary-row">
          <span class="itin-time">${item.time}</span>
          <span class="itin-act">${item.activity}</span>
        </div>
      `).join("");

      const mapQuery = encodeURIComponent(data.kakaoQuery || data.destination);

      resultBox.innerHTML = `
        <div class="curation-card">
          <div class="curation-badge">AI CURATOR'S PICK</div>
          <h2 class="curation-destination">${data.destination}</h2>
          <p class="curation-tagline">“${data.tagline}”</p>
          
          <div class="curation-section">
            <h4>💡 큐레이션 배경</h4>
            <p class="curation-reason">${data.reason}</p>
          </div>

          <div class="curation-section">
            <h4>📍 꼭 들러야 할 추천 스팟</h4>
            <div class="highlights-container">${highlightsHtml}</div>
          </div>

          <div class="curation-section">
            <h4>🗓 추천 동선 가이드</h4>
            <div class="itinerary-container">${itineraryHtml}</div>
          </div>

          <div class="curation-tip-box">
            <strong>🌿 큐레이터 꿀팁</strong>
            <p>${data.curatorTip}</p>
          </div>

          <div class="card-footer-actions">
            <a href="https://map.kakao.com/link/search/${mapQuery}" target="_blank" rel="noopener noreferrer" class="map-link-btn">
              🗺 카카오맵에서 위치 및 길찾기 보기 ↗
            </a>
          </div>
        </div>
      `;

      resultBox.style.display = "block";
      resultBox.scrollIntoView({ behavior: "smooth", block: "start" });

    } catch (err) {
      console.error(err);
      statusMsg.textContent = "일정을 분석하는 도중 문제가 생겼습니다. 다시 시도해 주세요.";
    } finally {
      submitBtn.disabled = false;
      btnText.textContent = "여행지 추천 받기";
    }
  });
});
