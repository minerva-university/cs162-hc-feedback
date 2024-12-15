// Store all examples globally for filtering
let allExamples = [];

// Add global context state
let currentContext = {
  assignmentDescription: "",
  existingContext: "",
};

document.addEventListener("DOMContentLoaded", function () {
  loadHCExamples();

  // Add click handlers for all modals
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        hideModal(modal.id);
      }
    });
  });

  // Add event listener for cornerstone filter
  document
    .getElementById("cornerstoneFilter")
    .addEventListener("change", filterHCs);

  // Add handbook link handler
  document.getElementById("handbookLink").onclick = showHandbookMessage;
});

async function loadHCExamples() {
  try {
    const response = await fetch("/api/hcs");
    const data = await response.json();

    // Flatten the data structure
    allExamples = Object.entries(data).flatMap(([cornerstone, hcs]) =>
      hcs.map((hc) => ({ ...hc, cornerstone: cornerstone }))
    );

    // Initial population of select
    updateHCSelect(allExamples);
  } catch (error) {
    console.error("Error loading HC examples:", error);
  }
}

function updateHCSelect(examples) {
  const select = document.getElementById("hcSelect");
  const footnoteButton = document.getElementById("footnoteButton"); // Add this line

  select.innerHTML = '<option value="">Select an HC example...</option>';

  examples.forEach((example) => {
    const option = document.createElement("option");
    option.value = example.hc_name;
    option.textContent = `${example.hc_name}`;
    select.appendChild(option);
  });

  // Add change event listener
  select.addEventListener("change", (e) => {
    if (e.target.value) {
      console.log("Selected HC:", e.target.value);
      footnoteButton.disabled = false; // Enable button when HC is selected
    } else {
      footnoteButton.disabled = true; // Disable button when no HC is selected
    }
  });

  // Disable footnote button by default
  footnoteButton.disabled = true;
}

function filterHCs() {
  const selectedCornerstone =
    document.getElementById("cornerstoneFilter").value;

  let filteredExamples = allExamples;
  if (selectedCornerstone) {
    filteredExamples = allExamples.filter(
      (example) => example.cornerstone === selectedCornerstone
    );
  }

  updateHCSelect(filteredExamples);
}

async function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modalId === "footnoteModal") {
    try {
      const selectedHC = document.getElementById("hcSelect").value;

      // Find the example in the allExamples array
      const example = allExamples.find((ex) => ex.hc_name === selectedHC);

      if (!example) {
        console.error("HC example not found:", selectedHC);
        return; // Or show an error message in the modal
      }

      const modalContent = modal.querySelector(".modal-content");
      modalContent.innerHTML = `
              <h2>Example: ${selectedHC}</h2>
              <div class="example-content">
                  <h3>General Example</h3>
                  <p>${example.general_example}</p>
              </div>
              <div class="footnote-content">
                  <h3>Footnote</h3>
                  <p>${example.footnote}</p>
              </div>
              <button onclick="hideModal('footnoteModal')" class="btn">Close</button>
          `;
    } catch (error) {
      console.error("Error showing example:", error);
    }
  }
  modal.classList.remove("hidden");
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}

function showHandbookMessage() {
  const selectedHC = document.getElementById("hcSelect").value;
  const handbookURL = `https://my.minerva.edu/application/login/?next=/academics/hc-resources/hc-handbook/#${selectedHC.toLowerCase()}`;
  window.open(handbookURL, "_blank");
}

async function submitFeedback(event) {
  event.preventDefault();

  const submitButton = event.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;
  submitButton.textContent = "Processing...";
  submitButton.disabled = true;

  const selectedHC = document.getElementById("hcSelect").value;
  const assignmentText = document.getElementById("assignmentText").value;

  try {
    // First, do the pre-check
    const precheckResponse = await fetch("/api/precheck", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: assignmentText }),
    });

    const precheckData = await precheckResponse.json();

    if (!precheckData.is_meaningful) {
      alert(`Input quality check failed: ${precheckData.feedback}`);
      return;
    }

    // Continue with the rest of the submission process
    const example = allExamples.find((ex) => ex.hc_name === selectedHC);
    console.log("Selected HC:", example);
    if (!example) {
      console.error("HC example not found:", selectedHC);
      alert("Please select an HC.");
      return;
    }

    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: assignmentText,
        hc_name: selectedHC, // Send the selected HC name to the backend
        guided_reflection: example.guided_reflection, // Send the guided reflection criteria
        common_pitfalls: example.common_pitfalls, // Send the common pitfalls
        context: currentContext, // Add context information
      }),
    });

    const data = await response.json();
    console.log(data);
    displayFeedback(data);
  } catch (error) {
    console.error("Error:", error);
    alert(`An error occurred: ${error.message}`); // Show the error's message
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
  document.getElementById("feedbackText").textContent =
    feedback.general_feedback; // Use general_feedback

  // Display actionable steps
  const stepsContainer = document.getElementById("actionableSteps");
  stepsContainer.innerHTML = ""; // Clear existing steps

  const actionableSteps = parseSpecificFeedback(feedback.specific_feedback);

  actionableSteps.forEach((step) => {
    const stepElement = document.createElement("div");
    stepElement.className = "step-item";

    stepElement.innerHTML = `
            <input type="checkbox" ${step.completed ? "checked" : ""}>
            <p><strong>Change:</strong> ${
              step.change
            }</p>  </p> <p><strong>From:</strong> ${
      step.from
    }</p><p><strong>To:</strong> ${step.to}</p>
            <div class="tooltip">
                ℹ️
                <span class="tooltip-text">${step.why}</span>
            </div>
        `; // Added elements for change, from, and to

    stepsContainer.appendChild(stepElement);
  });
}

function parseSpecificFeedback(feedbackString) {
  const steps = [];
  const regex =
    /- \[(x| )] Change: (.+)\n  From: (.+)\n  To: (.+)\n  Why: (.+)/g; // Modified regex
  let match;

  while ((match = regex.exec(feedbackString)) !== null) {
    steps.push({
      change: match[2].trim(), // Capture "Change"
      from: match[3].trim(), // Capture "From"
      to: match[4].trim(), // Capture "To"
      why: match[5].trim(), // Capture "Why"
      completed: match[1] === "x",
    });
  }
  return steps;
}

function saveContext() {
  currentContext = {
    assignmentDescription: document.getElementById("assignmentDescription")
      .value,
    existingContext: document.getElementById("existingContext").value,
  };
  hideModal("contextModal");

  // Update the context button to show status
  const contextButton = document.querySelector(
    'button[onclick="showModal(\'contextModal\')"]'
  );
  contextButton.classList.add("has-context");
  contextButton.textContent = "Update Context";
}
