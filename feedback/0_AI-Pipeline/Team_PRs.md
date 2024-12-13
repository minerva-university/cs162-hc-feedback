> !! These are AI generated, so please look my video for more info.

<div>
    <a href="https://www.loom.com/share/a7f95fe1dc1747bbada02ff783e42d8a">
      <p>Feedback Tool Demo 🎥 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/a7f95fe1dc1747bbada02ff783e42d8a">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/a7f95fe1dc1747bbada02ff783e42d8a-f07eabd02bc0292e-full-play.gif">
    </a>
  </div>

# Backend PRs

## 1. Logging Enhancement @uliana1one

**Title:** `feat/HFC-1/enhance-logging`

**Description:**  Replace `print` statements with proper logging using Python's `logging` module. Implement log levels (DEBUG, INFO, ERROR). Create a consistent log format. Add log file configuration in `feedback/0_AI-Pipeline/config.py`.

**Acceptance Criteria:**

- All `print` statements are replaced with appropriate logging calls.
- Log messages include timestamps and relevant context.
- Log levels are correctly used to categorize messages.
- Log output can be directed to the console or a file via configuration.  A configuration file exists for log settings.

**Expected Tests:**

- Test that log messages are written to the expected location (console or file).
- Test that log messages include the correct timestamp and log level.
- Test that log messages contain expected context information.
- Test configuration file allows change of log level and output location.


## 2. Code Refactoring @Taka0613

**Title:** `refactor/HFC-2/pipeline-structure`

**Description:** Move `evaluate_pitfall` function. Clean up duplicate functions. Standardize error handling. Add type hints.

**Acceptance Criteria:**

- `evaluate_pitfall` is moved to `evaluation.py`.
- Duplicate code is removed or refactored into reusable functions.  Code duplication reduced by at least 20%.
- Consistent error handling is implemented throughout the codebase.
- Type hints are added to all functions and their parameters.

**Expected Tests:**

- Test that `evaluate_pitfall` functions correctly after relocation.
- Unit tests for all refactored functions to verify correct functionality.
- Test that error handling functions correctly for expected exceptions.
- Static code analysis to verify type hints are correctly applied.


## 3. Dynamic HC Integration @dilnazua

**Title:** `feat/HFC-3/dynamic-hc-integration`

**Description:** Refactor feedback system to dynamically load evaluation criteria and pitfalls from database. Enable CRUD operations for managing criteria.

**Acceptance Criteria:**

- Sample (AI-Generated):
  ```python
  class EvaluationCriteria(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      type = db.Column(db.String) # 'guided' or 'pitfall'
      text = db.Column(db.Text)
      active = db.Column(db.Boolean, default=True)

  class FeedbackResult(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      thesis_text = db.Column(db.Text)
      criteria_id = db.Column(db.Integer, db.ForeignKey('evaluation_criteria.id'))
      passed = db.Column(db.Boolean)
      feedback = db.Column(db.Text)

**Expected Tests:**

- Test database connection establishment.
- Test that all database tables are correctly created.
- Unit tests for each CRUD operation (create, read, update, delete).
- Integration tests verifying the interaction between the application and database.


# Frontend PRs

## 4. Base UI Implementation @CarlKho-Minerva

**Title:** `feat/HFC-4/base-ui`

**Description:** Update `index.html`. Style feedback components. Implement responsive design.

**Acceptance Criteria:**

- `index.html` is updated with a new layout for feedback display.
- Feedback components are styled consistently with the application's design.
- The UI is responsive and adapts to different screen sizes.

**Expected Tests:**

- Visual inspection for correct layout and styling.
- Browser testing to verify responsive behavior on different devices/screen sizes.


## 5. General Feedback Display @ayaelnakeb

**Title:** `feat/HFC-5/general-feedback`

**Description:** Create general_feedback component.

**Acceptance Criteria:**

- A clear and visually appealing component is created for displaying general feedback.
- The component is styled consistently with the application's design.

**Expected Tests:**

- Visual inspection for clear display of feedback and score.


## 6. Checklist Integration @elbionredenica

**Title:** `feat/HFC-6/checklist-ui`

**Description:** Implement checklist component. Add checkbox functionality. Style checklist items.

**Acceptance Criteria:**

- Checklist component displays "From" and "To" sections clearly.
- Checkboxes allow users to mark items as complete.
- Checklist items are styled consistently with the application's design.

**Expected Tests:**

- Test that checkboxes function correctly.
- Verify that checklist items are displayed correctly.


## 7. Tooltip Enhancement @ayaelnakeb

**Title:** `feat/HFC-7/tooltips`

**Description:** Add tooltips to "Why" section. Implement hover functionality. Style tooltip components.

**Acceptance Criteria:**

- Tooltips provide concise explanations for each "Why" section.
- Tooltips appear on hover and disappear when the mouse moves away.
- Tooltips are styled consistently with the application's design.

**Expected Tests:**

- Verify tooltip appearance on hover and disappearance on mouse-out.
- Verify tooltip content is correct.


## 8. Text Highlight Feature (Optional)

**Title:** `feat/HFC-8/text-highlights`

**Description:** Add text difference highlighting using regex. Highlight changed sections. Add visual indicators.

**Acceptance Criteria:**

- Added, removed, and changed text segments are clearly highlighted.
- Different visual indicators (e.g., colors) are used to distinguish between changes.
- The highlighting does not interfere with the readability of the text.

**Expected Tests:**

- Test that text highlighting functions correctly for various input strings.
- Verify that different types of changes (added, removed, changed) are correctly highlighted.


# Testing PRs

## 9. Test Suite Implementation @CarlKho-Minerva

**Title:** `test/HFC-9/test-coverage`

**Description:** Add pytest fixtures. Write unit tests. Add integration tests. Mock AI responses.

**Acceptance Criteria:**

- A comprehensive suite of unit and integration tests is implemented.
- Test coverage reaches at least 80%.
- Tests are designed to cover various scenarios and edge cases.
- AI responses are mocked to avoid dependency on external APIs during testing.

**Expected Tests:**

- Test suite runs without errors.
- Test report shows at least 80% code coverage.  Specific coverage targets might be adjusted based on needs.