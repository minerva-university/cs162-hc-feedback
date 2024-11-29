document.addEventListener("DOMContentLoaded", function () {
    // Remove or comment out initializeSearch() since we removed the search bar
    // initializeSearch();
    loadHCExamples();
});

// Remove or comment out the initializeSearch function since it's no longer needed
/*
function initializeSearch() {
    const searchInput = document.getElementById("searchHCs");
    searchInput.addEventListener("input", function (e) {
        console.log("Searching for:", e.target.value);
    });
}
*/

async function loadHCExamples() {
  try {
    const response = await fetch("/api/hc-examples");
    const examples = await response.json();
    const select = document.getElementById("hcSelect");

    examples.forEach((example) => {
      const option = document.createElement("option");
      option.value = example.hc_name;
      option.textContent = example.hc_name;
      select.appendChild(option);
    });

    // Remove the automatic modal trigger
    // Just log that the selection changed
    select.addEventListener("change", (e) => {
      if (e.target.value) {
        console.log("Selected HC:", e.target.value);
      }
    });
  } catch (error) {
    console.error("Error loading HC examples:", error);
  }
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
  document.getElementById(modalId).classList.add("hidden");
}
function showHandbookMessage() {
  const handbookModal = document.getElementById("handbookModal");
  handbookModal.classList.remove("hidden");
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
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
