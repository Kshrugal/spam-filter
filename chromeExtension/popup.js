document.getElementById("checkBtn").addEventListener("click", async () => {
  const message = document.getElementById("message").value.trim();
  const resultEl = document.getElementById("result");

  if (!message) {
    resultEl.textContent = "⚠️ Please enter a message!";
    resultEl.style.color = "orange";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    if (data.prediction) {
      if (data.prediction === "spam") {
        resultEl.textContent = `This looks like SPAM! (Confidence: ${data.confidence}%)`;
        resultEl.style.color = "red";
      } else {
        resultEl.textContent = `This looks like HAM (not spam). (Confidence: ${data.confidence}%)`;
        resultEl.style.color = "green";
      }
    } else {
      resultEl.textContent = "Error: " + (data.error || "Unknown issue");
      resultEl.style.color = "orange";
    }
  } catch (err) {
    resultEl.textContent = "Could not connect to API. Make sure it's running!";
    resultEl.style.color = "orange";
  }
});
