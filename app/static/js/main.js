// Store all examples globally for filtering
let allExamples = [];

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
  document.getElementById('toggleLog').addEventListener('click', function() {
    const log = document.getElementById('processingLog');
    const btn = document.getElementById('toggleLog');
    if (log.classList.contains('hidden')) {
        log.classList.remove('hidden');
        btn.textContent = 'Hide Processing Log';
    } else {
        log.classList.add('hidden');
        btn.textContent = 'Show Processing Log';
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
  const handbookURL = `https://my.minerva.edu/application/login/?next=/academics/hc-resources/hc-handbook/#${selectedHC.toLowerCase()}`;
  window.open(handbookURL, "_blank");
}

function addLogEntry(message, type = 'status') {
    const log = document.getElementById('processingLog');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;

    const time = document.createElement('span');
    time.className = 'log-time';
    time.textContent = new Date().toLocaleTimeString();

    const msg = document.createElement('span');
    msg.className = 'log-message';
    msg.textContent = message;

    entry.appendChild(time);
    entry.appendChild(msg);
    log.appendChild(entry);
    log.scrollTop = log.scrollHeight;
}

function updateProgress(percent, status, logMessage, type = 'status') {
    const progressSection = document.getElementById('progressSection');
    const progressBar = document.getElementById('progressBar');
    const progressStatus = document.getElementById('progressStatus');

    progressSection.classList.remove('hidden');
    progressBar.style.width = `${percent}%`;
    progressStatus.textContent = status;

    // Update phase indicators
    updatePhaseIndicators(percent);

    if (logMessage) {
        addLogEntry(logMessage, type);
    }
}

function updatePhaseIndicators(percent) {
    const phases = document.querySelectorAll('.phase-step');
    phases.forEach((phase, index) => {
        const phaseThreshold = (index + 1) * (100 / phases.length);
        if (percent >= phaseThreshold) {
            phase.classList.add('completed');
            phase.classList.remove('active');
        } else if (percent >= phaseThreshold - (100 / phases.length)) {
            phase.classList.add('active');
            phase.classList.remove('completed');
        } else {
            phase.classList.remove('active', 'completed');
        }
    });
}

async function submitFeedback(event) {
    event.preventDefault();

    // Reset progress section and show it
    const progressSection = document.getElementById('progressSection');
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
    progressSection.classList.remove('hidden');

    // Reattach toggle event listener
    document.getElementById('toggleLog').addEventListener('click', function() {
        const log = document.getElementById('processingLog');
        this.textContent = log.classList.toggle('hidden') ?
            'Show Processing Details' : 'Hide Processing Details';
    });

    // Rest of the submission logic with more detailed logging
    try {
        updateProgress(5, 'Initializing...', 'Starting feedback process', 'info');
        // ...existing try block code but with more granular progress updates:

        updateProgress(15, 'Analyzing input...', 'Checking input quality and formatting', 'info');
        // Precheck API call...

        updateProgress(30, 'Validating content...', 'Evaluating academic content standards', 'info');
        // More detailed validation logs...

        updateProgress(45, 'Processing HC criteria...', 'Analyzing against selected HC requirements', 'info');
        // HC processing...

        updateProgress(60, 'Generating feedback...', 'Creating personalized feedback', 'info');
        // Feedback generation...

        updateProgress(85, 'Finalizing...', 'Formatting results and recommendations', 'info');
        // Final processing...

        updateProgress(100, 'Complete!', 'Analysis completed successfully', 'status');

    } catch (error) {
        updateProgress(100, 'Error occurred', error.message, 'error');
        console.error("Error:", error);
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
