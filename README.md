# HC Feedback System

A Flask-based web application for providing automated feedback on assignments.

## Project Structure

```
cs162-hc-feedback/
├── README.md               # Main documentation
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
├── Dockerfile              # Docker configuration
├── app/                    # Application package
│   ├── __init__.py         # App initialization
│   ├── routes.py           # Route definitions
│   ├── static/             # Static files (CSS, JS)
│   ├── templates/          # HTML templates
│   ├── AI/                 # AI-related modules
│   └── utils/              # Utility functions and helpers
├── archive/                # Archived files and old versions
├── docs/                   # Additional documentation
│   └── CONTRIBUTING.md     # Contribution guidelines
├── feedback/               # Feedback-related modules
└── tests/                  # Unit and integration tests
```

### Detailed Explanation

- **README.md**: This file. It contains the main documentation for the project.
- **requirements.txt**: Lists all the Python dependencies required for the project.
- **run.py**: The entry point for the application. It initializes the Flask app and starts the server.
- **Dockerfile**: Configuration file for Docker, used to containerize the application.
- **app/**: The main application package.
  - **\_\_init\_\_.py**: Initializes the Flask app and sets up configurations.
  - **routes.py**: Defines the routes/endpoints for the application.
  - **static/**: Contains static files like CSS and JavaScript.
  - **templates/**: Contains HTML templates for rendering web pages.
  - **AI/**: Contains modules related to AI functionalities, such as models and processing scripts.
  - **utils/**: Contains utility functions and helper scripts during the development of the application.
- **archive/**: Contains archived files and old versions of the project for reference.
- **docs/**: Contains additional documentation.
  - **CONTRIBUTING.md**: Guidelines for contributing to the project.
- **feedback/**: Contains modules related to feedback processing and generation.
- **tests/**: Contains unit tests to ensure the application works as expected.

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

4. Set the .env variables:
Follow the structure below: 

 ```bash
GENAI_API_KEY="" # Your GenAI API key - ideally gemini-1.5-flash-8b
GEMINI_MODEL_NAME="gemini-1.5-flash"
SCORE_THRESHOLD=0.8 # For footnote generator
 ```

6. Run the application:

   ```bash
   python run.py
   ```

7. Visit `http://127.0.0.1:8080` in your browser. The app is also deployed on http://hc-feedback.duckdns.org/ for development
 and on http://hc-feedback-tool.duckdns.org/ for production.

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
