
// Update the "View in HC Handbook" button with onclick
document.getElementById("handbookLink").onclick = showHandbookMessage;

// Store all examples globally for filtering
let allExamples = [];

document.addEventListener("DOMContentLoaded", function () {
document.addEventListener("DOMContentLoaded", function () {
  // Initialize necessary components
  initializeSearch();
  initializeGeneralFeedback();
  loadHCExamples();

  // Add click handlers for all modals
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", (e) => {
      // Close if clicking outside the modal content
      if (e.target === modal) {
        hideModal(modal.id);
      }
    });
  });

  // Add event listeners for search and cornerstone filter
  document.getElementById("cornerstoneFilter").addEventListener("change", filterHCs);
});


async function loadHCExamples() {
  try {
      const response = await fetch("/api/hc-examples");
      allExamples = await response.json();
      updateHCSelect(allExamples);
  } catch (error) {
      console.error("Error loading HC examples:", error);
  }
}

function updateHCSelect(examples) {
  const select = document.getElementById("hcSelect");
  select.innerHTML = '<option value="">Select an HC example...</option>';

  examples.forEach(example => {
      const option = document.createElement("option");
      option.value = example.hc_name;
      option.textContent = `${example.hc_name}`;
      select.appendChild(option);
  });

  // Add change event listener
  select.addEventListener("change", (e) => {
      if (e.target.value) {
          console.log("Selected HC:", e.target.value);
      }
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

function filterHCs() {
  const selectedCornerstone = document.getElementById("cornerstoneFilter").value;

  const filteredExamples = allExamples.filter(example => {
    const matchesCornerstone = !selectedCornerstone || example.cornerstone === selectedCornerstone;
    return matchesCornerstone;
  });

  updateHCSelect(filteredExamples);
}

async function showModal(modalId) {
  const modal = document.getElementById(modalId);

  if (modalId === "footnoteModal") {
    try {
      const selectedHC = document.getElementById("hcSelect").value;
      const response = await fetch(`/api/hc-example/${selectedHC}`);
      const data = await response.json();

      const modalContent = modal.querySelector(".modal-content");
      modalContent.innerHTML = `
        <h2>Example: ${selectedHC}</h2>
        <div class="example-content">
          <h3>General Example</h3>
          <p>${data.general_example}</p>
        </div>
        <div class="footnote-content">
          <h3>Footnote</h3>
          <p>${data.footnote}</p>
        </div>
        <button onclick="hideModal('footnoteModal')" class="btn">Close</button>
      `;
    } catch (error) {
      console.error("Error fetching example:", error);
    }
  }

  modal.classList.remove("hidden");
}

function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.add("hidden");
}


function hideModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}

function showHandbookMessage() {
  const handbookModal = document.getElementById("handbookModal");
  handbookModal.classList.remove("hidden");
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