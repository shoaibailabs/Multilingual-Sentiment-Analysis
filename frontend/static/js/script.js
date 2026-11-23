
const textInput = document.getElementById("textInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const resultCard = document.getElementById("resultCard");

const sentimentResult = document.getElementById("sentimentResult");
const confidenceResult = document.getElementById("confidenceResult");


analyzeBtn.addEventListener("click", async function () {

    const text = textInput.value.trim();

    // Check empty input
    if (!text) {
        showError("Please enter a comment first.");
        return;
    }

    // Reset previous results
    errorMessage.classList.add("hidden");
    resultCard.classList.add("hidden");

    loading.classList.remove("hidden");
    analyzeBtn.disabled = true;

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        // Show sentiment
        const sentiment = String(
            data.sentiment || data.prediction || "Unknown"
        );

        sentimentResult.textContent =
            sentiment.charAt(0).toUpperCase() + sentiment.slice(1);

        // Show confidence
        let confidence = data.confidence;

        if (confidence === undefined) {
            confidence = data.confidence_score;
        }

        if (typeof confidence === "number") {
            confidenceResult.textContent =
                (confidence <= 1
                    ? confidence * 100
                    : confidence
                ).toFixed(2) + "%";
        } else {
            confidenceResult.textContent = "Not available";
        }

        resultCard.classList.remove("hidden");

    } catch (error) {

        showError(error.message);

    } finally {

        loading.classList.add("hidden");
        analyzeBtn.disabled = false;

    }

});


// Clear button
clearBtn.addEventListener("click", function () {

    textInput.value = "";

    resultCard.classList.add("hidden");
    errorMessage.classList.add("hidden");
    loading.classList.add("hidden");

    analyzeBtn.disabled = false;

});


// Display error
function showError(message) {

    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");

}
