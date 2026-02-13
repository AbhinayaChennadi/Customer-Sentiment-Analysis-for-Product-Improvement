console.log("script.js loaded");

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("reviewForm");
    const resultDiv = document.getElementById("result");
    const errorDiv = document.getElementById("errorMessage");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Clear previous messages
        resultDiv.innerHTML = "";
        errorDiv.innerText = "";

        // Get raw text and split by new lines
        const rawText = document.getElementById("review").value;

        // Split into array of non-empty lines
        const texts = rawText
            .split("\n")
            .map(t => t.trim())
            .filter(t => t.length > 0);

        if (texts.length === 0) {
            errorDiv.innerText = "Please enter at least one review.";
            return;
        }

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ texts: texts })
            });

            const data = await response.json();
            console.log("🔥 Response from server:", data);

            if (!data.results || !Array.isArray(data.results)) {
                errorDiv.innerText = "Error: Invalid response from server.";
                console.error("Invalid response:", data);
                return;
            }

            // Create a <pre> inside resultDiv to preserve line breaks
            const pre = document.createElement("pre");
            pre.style.whiteSpace = "pre-wrap"; // wrap long lines
            pre.style.fontSize = "16px";
            pre.style.lineHeight = "1.5";
            resultDiv.appendChild(pre);

            // Display each review line by line
            data.results.forEach(item => {
                pre.innerText += `"${item.text}" → Sentiment: ${item.sentiment} (Score: ${item.score.toFixed(2)})\n`;
            });

            // Add summary counts
            pre.innerText += "\nSummary:\n";
            pre.innerText += `Positive: ${data.summary.Positive}\n`;
            pre.innerText += `Negative: ${data.summary.Negative}\n`;
            pre.innerText += `Neutral: ${data.summary.Neutral}\n`;

            // Add management suggestion
            pre.innerText += `\nManagement Suggestion:\n${data.suggestion}\n`;

        } catch (err) {
            errorDiv.innerText = "Error: " + err.message;
            console.error("Fetch error:", err);
        }
    });
});
