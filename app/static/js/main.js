// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  // Initialize any necessary components
  initializeSearch();
  initializeGeneralFeedback();
});

function initializeSearch() {
  const searchInput = document.getElementById("searchHCs");
  searchInput.addEventListener("input", function (e) {
    // Implement search functionality here
    console.log("Searching for:", e.target.value);
  });
}

function initializeGeneralFeedback() {
  const feedbackToggle = document.getElementById("generalFeedbackToggle");
  const feedbackContainer = document.getElementById("generalFeedbackContainer");

  feedbackToggle.addEventListener("click", async function () {
    if (feedbackContainer.classList.contains("hidden")) {
      // Show feedback
      await fetchGeneralFeedback();
      feedbackContainer.classList.remove("hidden");
      feedbackToggle.textContent = "Hide General Feedback";
    } else {
      // Hide feedback
      feedbackContainer.classList.add("hidden");
      feedbackToggle.textContent = "View General Feedback";
    }
  });
}
async function fetchGeneralFeedback() {
  const feedbackContainer = document.getElementById("generalFeedbackContainer");

  try {
    const response = await fetch("/api/general_feedback", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const feedback = await response.json();
      displayGeneralFeedback(feedback);
    } else {
      console.error("Failed to fetch general feedback");
      feedbackContainer.innerHTML = `<p>Error fetching feedback. Please try again later.</p>`;
    }
  } catch (error) {
    console.error("Error:", error);
    feedbackContainer.innerHTML = `<p>An error occurred while fetching feedback.</p>`;
  }
}
function displayGeneralFeedback(feedback) {
  const feedbackText = document.getElementById("generalFeedbackText");
  const feedbackScore = document.getElementById("generalFeedbackScore");

  feedbackText.textContent = feedback.text || "No feedback available.";
  feedbackScore.textContent = `Score: ${feedback.score || "N/A"}`;
}


function showModal(modalId) {
  document.getElementById(modalId).classList.remove("hidden");
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}
function showHandbookMessage() {
  const handbookModal = document.getElementById('handbookModal');
  handbookModal.classList.remove('hidden');
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
}

// Update the "View in HC Handbook" button with onclick
document.getElementById("handbookLink").onclick = showHandbookMessage;



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
