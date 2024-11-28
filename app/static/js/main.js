// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  // Initialize any necessary components
  initializeSearch();
});

function initializeSearch() {
  const searchInput = document.getElementById("searchHCs");
  searchInput.addEventListener("input", function (e) {
    // Implement search functionality here
    console.log("Searching for:", e.target.value);
  });
}

function showModal(modalId) {
  document.getElementById(modalId).classList.remove("hidden");
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
}

async function submitFeedback(event) {
  event.preventDefault();

  // Show loading state
  const submitButton = event.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;
  submitButton.textContent = "Processing...";
  submitButton.disabled = true;

  try {
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: document.getElementById("assignmentText").value,
      }),
    });

    const data = await response.json();
    displayFeedback(data);
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while processing your feedback request.");
  } finally {
    submitButton.textContent = originalText;
    submitButton.disabled = false;
  }
}

function displayFeedback(feedback) {
  // Show feedback container
  const resultsContainer = document.getElementById("feedbackResults");
  resultsContainer.classList.remove("hidden");

  // Display main feedback text
  document.getElementById("feedbackText").textContent = feedback.text;

  // Display actionable steps
  const stepsContainer = document.getElementById("actionableSteps");
  stepsContainer.innerHTML = ""; // Clear existing steps

  feedback.actionable_steps.forEach((step) => {
    const stepElement = document.createElement("div");
    stepElement.className = "step-item";

    stepElement.innerHTML = `
            <input type="checkbox">
            <span>${step.text}</span>
            <div class="tooltip">
                ℹ️
                <span class="tooltip-text">${step.tooltip}</span>
            </div>
        `;

    stepsContainer.appendChild(stepElement);
  });
}
