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

  // Add after DOMContentLoaded event listener
  document.getElementById("toggleLog").addEventListener("click", function () {
    const log = document.getElementById("processingLog");
    const btn = document.getElementById("toggleLog");
    if (log.classList.contains("hidden")) {
      log.classList.remove("hidden");
      btn.textContent = "Hide Processing Log";
    } else {
      log.classList.add("hidden");
      btn.textContent = "Show Processing Log";
    }
  });
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
  const handbookURL = `https://my.minerva.edu/application/login/?next=/academics/hc-resources/hc-handbook/${selectedHC.toLowerCase()}`;
  window.open(handbookURL, "_blank");
}

function addLogEntry(message, type = "status", subphase = "") {
  const log = document.getElementById("processingLog");
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;

  const time = document.createElement("span");
  time.className = "log-time";
  time.textContent = new Date().toLocaleTimeString([], { hour12: false });

  const msg = document.createElement("span");
  msg.className = "log-message";

  // Add subphase prefix if provided
  const prefix = subphase ? `[${subphase}] ` : "";
  msg.innerHTML = `${prefix}${message}`;

  entry.appendChild(time);
  entry.appendChild(msg);
  log.appendChild(entry);
  log.scrollTop = log.scrollHeight;
}

function updateProgress(percent, status, logMessage, type = "status") {
  const progressSection = document.getElementById("progressSection");
  const progressBar = document.getElementById("progressBar");
  const progressStatus = document.getElementById("progressStatus");

  progressSection.classList.remove("hidden");
  progressBar.style.width = `${percent}%`;
  progressStatus.textContent = status;

  // Update phase indicators
  updatePhaseIndicators(percent);

  if (logMessage) {
    addLogEntry(logMessage, type);
  }
}

function updatePhaseIndicators(percent) {
  const phases = document.querySelectorAll(".phase-step");
  phases.forEach((phase, index) => {
    const phaseThreshold = (index + 1) * (100 / phases.length);
    if (percent >= phaseThreshold) {
      phase.classList.add("completed");
      phase.classList.remove("active");
    } else if (percent >= phaseThreshold - 100 / phases.length) {
      phase.classList.add("active");
      phase.classList.remove("completed");
    } else {
      phase.classList.remove("active", "completed");
    }
  });
}

async function submitFeedback(event) {
  event.preventDefault();
  const startTime = Date.now();

  const submitButton = event.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;
  submitButton.textContent = "Processing...";
  submitButton.disabled = true;

  // Reset and initialize progress section
  const progressSection = document.getElementById("progressSection");
  progressSection.innerHTML = `
        <div class="phase-indicator">
            <div class="phase-step">Input Analysis</div>
            <div class="phase-step">Content Validation</div>
            <div class="phase-step">HC Processing</div>
            <div class="phase-step">Feedback Generation</div>
        </div>
        <div class="progress-container">
            <div id="progressBar" class="progress-bar"></div>
        </div>
        <p id="progressStatus" class="progress-status">Initializing...</p>
        <button id="toggleLog" class="toggle-log-btn">Show Processing Details</button>
        <div id="processingLog" class="processing-log hidden"></div>
    `;
  progressSection.classList.remove("hidden");

  // Reattach toggle event listener
  document.getElementById("toggleLog").addEventListener("click", function () {
    const log = document.getElementById("processingLog");
    this.textContent = log.classList.toggle("hidden")
      ? "Show Processing Details"
      : "Hide Processing Details";
  });

  const selectedHC = document.getElementById("hcSelect").value;
  const assignmentText = document.getElementById("assignmentText").value;

  try {
    // Initial setup
    updateProgress(
      2,
      "Initializing analysis...",
      "Initializing feedback system",
      "info",
      "Setup"
    );
    addLogEntry("Validating submission requirements", "info", "Setup");
    addLogEntry(`Selected HC: ${selectedHC}`, "info", "Setup");
    addLogEntry(
      `Input length: ${assignmentText.length} characters`,
      "info",
      "Setup"
    );

    // Input Quality Check Phase
    updateProgress(
      10,
      "Checking input quality...",
      "Starting input quality assessment",
      "info",
      "Quality Check"
    );
    addLogEntry(
      "Analyzing text structure and content",
      "info",
      "Quality Check"
    );

    const precheckResponse = await fetch("/api/precheck", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: assignmentText }),
    });

    const precheckData = await precheckResponse.json();
    updateProgress(
      20,
      "Input quality check complete",
      "Quality check completed",
      "status",
      "Quality Check"
    );
    addLogEntry(
      `Quality check result: ${
        precheckData.is_meaningful ? "Passed" : "Failed"
      }`,
      precheckData.is_meaningful ? "status" : "error",
      "Quality Check"
    );

    if (precheckData.is_meaningful) {
      addLogEntry(
        "Carl and team wishes you good luck! 🍀",
        "status",
        "Message"
      );
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Pause for effect
    }

    if (!precheckData.is_meaningful) {
      updateProgress(
        100,
        "Input check failed",
        precheckData.feedback,
        "error",
        "Quality Check"
      );
      addLogEntry(
        "Process terminated: Input quality requirements not met",
        "error",
        "Quality Check"
      );
      alert(`Input quality check failed: ${precheckData.feedback}`);
      return;
    }

    // HC Validation Phase
    updateProgress(
      30,
      "Validating HC criteria...",
      "Loading HC requirements",
      "info",
      "HC Validation"
    );
    addLogEntry("Obtaining data from HC Handbook...", "info", "HC Validation");
    addLogEntry(
      "Accessing: https://my.minerva.edu/academics/hc-resources/hc-handbook/",
      "info",
      "Source"
    );
    const example = allExamples.find((ex) => ex.hc_name === selectedHC);
    if (!example) {
      throw new Error("Selected HC configuration not found");
    }
    addLogEntry(
      "HC requirements loaded successfully",
      "status",
      "HC Validation"
    );
    addLogEntry(
      `Processing ${example.guided_reflection.length} reflection criteria`,
      "info",
      "HC Validation"
    );
    addLogEntry(
      `Checking ${example.common_pitfalls.length} common pitfalls`,
      "info",
      "HC Validation"
    );

    // Analysis Phase - More Granular
    updateProgress(
      45,
      "Initializing AI pipeline...",
      "Starting analysis sequence",
      "info",
      "Analysis"
    );
    addLogEntry("Loading AI models...", "info", "AI Setup");
    addLogEntry("Initializing Gemini-1.5-flash model...", "info", "AI Setup");
    addLogEntry("Configuring analysis parameters...", "info", "AI Setup");
    await new Promise((resolve) => setTimeout(resolve, 500)); // Visual pause

    updateProgress(
      50,
      "Processing content...",
      "Running primary analysis",
      "info",
      "Analysis"
    );
    addLogEntry("Phase 1: Analyzing semantic structure...", "info", "Analysis");
    addLogEntry(
      "Phase 2: Evaluating contextual relevance...",
      "info",
      "Analysis"
    );

    updateProgress(
      55,
      "Processing HC criteria...",
      "Analyzing reflection criteria",
      "info",
      "Analysis"
    );
    example.guided_reflection.forEach((criterion, index) => {
      addLogEntry(
        `Evaluating criterion ${index + 1}/${
          example.guided_reflection.length
        }...`,
        "info",
        "Analysis"
      );
    });

    updateProgress(
      60,
      "Processing pitfalls...",
      "Checking common pitfalls",
      "info",
      "Analysis"
    );
    example.common_pitfalls.forEach((pitfall, index) => {
      addLogEntry(
        `Checking pitfall ${index + 1}/${example.common_pitfalls.length}...`,
        "info",
        "Analysis"
      );
    });

    addLogEntry(
      "Starting API request for detailed analysis...",
      "info",
      "Analysis"
    );
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: assignmentText,
        hc_name: selectedHC, // Send the selected HC name to the backend
        guided_reflection: example.guided_reflection, // Send the guided reflection criteria
        common_pitfalls: example.common_pitfalls, // Send the common pitfalls
        context: currentContext, // Add context information
      }),
    });

    // Feedback Processing Phase - More Granular
    updateProgress(
      70,
      "Processing AI results...",
      "Analyzing AI output",
      "info",
      "Processing"
    );
    addLogEntry("Receiving AI model response...", "info", "Processing");
    const data = await response.json();
    addLogEntry("AI response received successfully", "status", "Processing");

    updateProgress(
      75,
      "Analyzing feedback...",
      "Processing feedback data",
      "info",
      "Processing"
    );
    addLogEntry("Calculating effectiveness scores...", "info", "Processing");
    addLogEntry("Organizing improvement suggestions...", "info", "Processing");

    updateProgress(
      80,
      "Generating recommendations...",
      "Creating actionable items",
      "info",
      "Processing"
    );
    addLogEntry("Formatting improvement steps...", "info", "Processing");
    addLogEntry("Prioritizing suggestions...", "info", "Processing");

    updateProgress(
      85,
      "Finalizing analysis...",
      "Preparing presentation",
      "info",
      "Formatting"
    );
    addLogEntry("Structuring feedback format...", "info", "Formatting");
    addLogEntry(
      "Generating actionable recommendations...",
      "info",
      "Formatting"
    );
    addLogEntry("Preparing final display...", "info", "Formatting");

    displayFeedback(data);

    // Enhanced Completion
    updateProgress(
      95,
      "Finalizing...",
      "Wrapping up analysis",
      "info",
      "Complete"
    );
    addLogEntry("Verifying all processes completed...", "info", "Complete");
    updateProgress(
      100,
      "Analysis complete",
      "Process completed successfully",
      "status",
      "Complete"
    );
    addLogEntry(
      "All analysis modules completed successfully",
      "status",
      "Complete"
    );
    addLogEntry(
      `Total processing time: ${((Date.now() - startTime) / 1000).toFixed(2)}s`,
      "info",
      "Complete"
    );
    addLogEntry("Thank you for using HC Feedback! 🎉", "status", "Complete");
  } catch (error) {
    console.error("Error:", error);
    updateProgress(100, "Error occurred", error.message, "error", "Error");
    addLogEntry(`Error details: ${error.message}`, "error", "Error");
    alert(`An error occurred: ${error.message}`);
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
