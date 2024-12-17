# Testing Guide

## Running Tests

### Basic Test Execution
```bash
# Run all tests (archive is automatically ignored via pytest.ini)
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_routes.py -v

# Run tests with print statements visible
pytest -s
```

### Coverage Testing
```bash
# Run tests with coverage report (excluding archive)
pytest --cov=app --ignore=tests/archive

# Generate HTML coverage report (excluding archive)
pytest --cov=app --cov-report=html --ignore=tests/archive

# Generate coverage with specific omissions
pytest --cov=app --cov-report=html --ignore=tests/archive --cov-config=.coveragerc
```

## Test Structure

### Model Tests (`test_models.py`)
Tests database models and relationships:
- Cornerstone creation and retrieval
- HC (Higher-level Criterion) creation and relationships
- Guided Reflection associations
- Common Pitfall associations
- Database constraints and cascading

### Route Tests (`test_routes.py`)
Tests API endpoints and web routes:
- Index page rendering
- HC retrieval by cornerstone
- All HCs retrieval
- Feedback API endpoint
- Precheck API endpoint
- Error handling and edge cases

### AI Agent Tests
#### Evaluation Tests (`test_agent_evaluation.py`)
- Individual criterion evaluation
- Multiple criteria evaluation
- Pass/Fail detection
- Error handling

#### Specific Feedback Tests (`test_agent_specific_feedback.py`)
- Feedback generation for criteria
- Pitfall evaluation
- Checklist formatting
- Context handling

#### General Feedback Tests (`test_agent_general_feedback.py`)
- General feedback generation
- Context incorporation
- Format validation

#### Precheck Tests (`test_agent_precheck.py`)
- Input quality validation
- Response format verification
- Error case handling

## Mock Testing
The tests use `unittest.mock` to:
- Mock AI model responses
- Simulate API calls
- Test error conditions
- Verify function calls

## Database Testing
Tests use SQLite in-memory database to:
- Ensure isolation between tests
- Speed up test execution
- Avoid affecting production data

## Logging in Tests
All tests include logging to:
- Track test execution
- Debug test failures
- Monitor database operations
- Verify AI model interactions

## Best Practices
1. Each test file focuses on a specific component
2. Tests are independent and isolated
3. Use fixtures for common setup
4. Mock external dependencies
5. Include both success and failure cases
6. Test edge cases and error conditions

## Common Test Commands
```bash
# Run tests matching a pattern (excluding archive)
pytest -k "test_routes" --ignore=tests/archive

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest --showlocals

# Run tests in parallel
pytest -n auto

# Generate JUnit XML report
pytest --junitxml=report.xml
```

## Debugging Tests
```bash
# Run with PDB on failures
pytest --pdb --ignore=tests/archive

# Get detailed logging output
pytest --log-cli-level=DEBUG --ignore=tests/archive

# Show test durations
pytest --durations=0 --ignore=tests/archive
```

## Continuous Integration
Tests are automatically run on:
- Pull requests
- Main branch commits
- Release tags

## Configuration
The project includes a pytest.ini file that:
- Automatically ignores Archive/archive directories
- Sets test discovery path to 'tests' directory
- Defines test file pattern as 'test_*.py'
- Excludes common directories (.*, venv)
