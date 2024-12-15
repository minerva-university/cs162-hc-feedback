
// Update the "View in HC Handbook" button with onclick
document.getElementById("handbookLink").onclick = showHandbookMessage;

// Store all examples globally for filtering
let allExamples = [];

document.addEventListener("DOMContentLoaded", function () {
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
      // Load HC data from the JSON file
      const response = await fetch("../static/js/all_hc_data.json");
      const data = await response.json();
      
      // Flatten the data structure (optional but recommended)
      allExamples = Object.values(data).flat();
  
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

          // Find the example in the allExamples array
          const example = allExamples.find(ex => ex.hc_name === selectedHC);

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
    window.open(handbookURL, '_blank');
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
        const example = allExamples.find(ex => ex.hc_name === selectedHC);
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
                common_pitfalls: example.common_pitfalls // Send the common pitfalls

            }),
        });
        
        const data = await response.json();
        console.log(data)
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
    document.getElementById("feedbackText").textContent = feedback.general_feedback; // Use general_feedback

    // Display actionable steps
    const stepsContainer = document.getElementById("actionableSteps");
    stepsContainer.innerHTML = ""; // Clear existing steps

    const actionableSteps = parseSpecificFeedback(feedback.specific_feedback);

    actionableSteps.forEach((step) => {
        const stepElement = document.createElement("div");
        stepElement.className = "step-item";

        stepElement.innerHTML = `
            <input type="checkbox" ${step.completed ? 'checked' : ''}>
            <p><strong>Change:</strong> ${step.change}</p>  </p> <p><strong>From:</strong> ${step.from}</p><p><strong>To:</strong> ${step.to}</p>
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
    const regex = /- \[(x| )] Change: (.+)\n  From: (.+)\n  To: (.+)\n  Why: (.+)/g; // Modified regex
    let match;

    while ((match = regex.exec(feedbackString)) !== null) {
        steps.push({
            change: match[2].trim(), // Capture "Change"
            from: match[3].trim(),   // Capture "From"
            to: match[4].trim(),     // Capture "To"
            why: match[5].trim(),     // Capture "Why"
            completed: match[1] === 'x'
        });
    }
    return steps;
}