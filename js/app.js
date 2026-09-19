(() => {
  const form = document.querySelector('#recommend-form');
  const submitButton = document.querySelector('#submit-button');
  const formMessage = document.querySelector('#form-message');
  const resultPanel = document.querySelector('#result-panel');
  const resultContent = document.querySelector('#result-content');
  const closeResult = document.querySelector('.close-result');

  const setMessage = (message, type = 'error') => {
    formMessage.textContent = message;
    formMessage.dataset.type = type;
  };

  const setLoading = (loading) => {
    submitButton.disabled = loading;
    submitButton.classList.toggle('is-loading', loading);
    submitButton.querySelector('.button-label').textContent = loading ? '여행지를 고르는 중...' : '여행지 추천 받기';
  };

  const showResult = (recommendation) => {
    const title = recommendation.title || '당신을 위한 국내 여행지';
    const description = recommendation.description || recommendation.reason || '';
    const reason = recommendation.reason ? `<p>${recommendation.reason}</p>` : '';
    const details = [recommendation.location, recommendation.best_time, recommendation.tip].filter(Boolean);
    resultContent.innerHTML = `<h3>${title}</h3><p>${description}</p>${reason}<div class="result-details">${details.map((detail) => `<span>${detail}</span>`).join('')}</div>`;
    resultPanel.hidden = false;
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    const missing = Object.values(payload).some((value) => !value.trim());

    if (missing) {
      setMessage('필수값을 입력하세요. 여행의 힌트를 모두 남겨주세요.');
      return;
    }

    setMessage('');
    setLoading(true);
    resultPanel.hidden = true;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || '추천을 가져오지 못했어요.');
      showResult(data.recommendation);
    } catch (error) {
      if (error.name === 'AbortError') {
        setMessage('응답이 조금 늦어지고 있어요. 잠시 후 다시 시도해 주세요.');
      } else {
        setMessage(error.message || '잠시 문제가 생겼어요. 다시 시도해 주세요.');
      }
    } finally {
      clearTimeout(timeoutId);
      setLoading(false);
    }
  });

  closeResult.addEventListener('click', () => { resultPanel.hidden = true; });
})();
