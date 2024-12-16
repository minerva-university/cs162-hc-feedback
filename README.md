# README.md

# HC Feedback System

A Flask-based web application for providing automated feedback on assignments.

## Project Structure

```
cs162-hc-feedback/
├── README.md               # Main documentation
├── requirements.txt        # Python dependencies
├── run.py                 # Application entry point
├── app/                   # Application package
│   ├── __init__.py       # App initialization
│   ├── routes.py         # Route definitions
│   ├── static/           # Static files (CSS, JS)
│   └── templates/        # HTML templates
└── docs/                 # Additional documentation
    └── CONTRIBUTING.md   # Contribution guidelines
```

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/minerva-university/cs162-hc-feedback.git
   cd cs162-hc-feedback
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python run.py
   ```

5. Visit `http://localhost:5000` in your browser.

## Development Guidelines

### Git Workflow

1. Create a new branch for each feature/bugfix:
For a feature:

   ```bash
   git checkout -b feature/TASK-NUMBER(e.g., HFC-0)/description
   ```

or for a bugfix:

   ```bash
   git checkout -b fix/TASK-NUMBER(e.g., HFC-0)/description
   ```

2. Make your changes and commit them:

   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push to your branch:

   ```bash
   git push origin [branch]
   ```

4. Create a Pull Request on GitHub.

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Write tests for new features

# Contributing to HC Feedback System

## Getting Started

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## Branch Naming Convention

- Feature branches: `feature/TASK-NUMBER(e.g., HFC-0)/description`
- Bug fixes: `fix/TASK-NUMBER(e.g., HFC-0)/description`
- Documentation: `docs/description`

`HFC` is the task name as per our Notion Kanban.

## Commit Naming Conventions

- Use the following prefixes for commit messages:
  - `feat`: A new feature (e.g., `feat: add user login functionality`)
  - `fix`: A bug fix (e.g., `fix: resolve issue with user authentication`)
  - `docs`: Documentation changes (e.g., `docs: update README with setup instructions`)
  - `style`: Code style changes (e.g., `style: format code according to PEP 8`)
  - `refactor`: Code refactoring without changing functionality (e.g., `refactor: simplify user service logic`)
  - `test`: Adding or updating tests (e.g., `test: add unit tests for user service`)
  - `chore`: Other changes that don't modify src or test files (e.g., `chore: update dependencies`)

- Use the imperative mood in the subject line (e.g., "Add feature" not "Added feature")
- Keep the subject line to 50 characters or less
- Separate the subject from the body with a blank line
- Use the body to explain what and why vs. how
- Reference relevant issues or pull requests

## Code Review Process

1. All code changes require a review from everyone
2. Address review comments promptly
3. Keep pull requests focused and small
4. Include tests for new features

## Best Practices

### Frontend

- Use semantic HTML
- Keep CSS classes modular
- Write clean, documented JavaScript
- Test across different browsers

### Backend

- Follow Flask best practices
- Document API endpoints
- Handle errors gracefully
- Write unit tests

### Git Commits

- Write clear commit messages
- Keep commits atomic
- Reference issues in commits

## Questions?

Feel free to open an issue for any questions or concerns.

