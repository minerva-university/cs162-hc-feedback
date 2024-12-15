# Thesis Evaluation Pipeline

<div>
    <a href="https://www.loom.com/share/a7f95fe1dc1747bbada02ff783e42d8a">
      <p>Feedback Tool Demo 🎥 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/a7f95fe1dc1747bbada02ff783e42d8a">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/a7f95fe1dc1747bbada02ff783e42d8a-f07eabd02bc0292e-full-play.gif">
    </a>
  </div>

An AI-powered system for evaluating and providing feedback on academic theses using Google's Gemini model.

## Overview

This pipeline:
1. Evaluates theses against standardized criteria
2. Identifies common pitfalls
3. Provides specific, actionable feedback
4. Generates line-by-line improvement suggestions

## Setup

1. Install dependencies:
```bash
pip install google-generativeai
```

2. Configure API key:
<div>
    <a href="https://www.loom.com/share/7cb6620021de496fab39517d45173a46">
      <p>AI Studio: Google's Developer Toolspace 🤖 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/7cb6620021de496fab39517d45173a46">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/7cb6620021de496fab39517d45173a46-d7c156d2c71c2401-full-play.gif">
    </a>
  </div>

- Get a Google AI API key from <https://aistudio.google.com/apikey>

- Add it to

`config.py`

```python
carl_api_key = "your-api-key-here"
```

## Usage

### Basic Evaluation

```python
from evaluation import evaluate_all_criteria

thesis = """Your thesis text here"""
results = evaluate_all_criteria(thesis)
```

### Detailed Feedback

```python
from specific_feedback import generate_checklist

feedback = generate_checklist(thesis)
print(feedback)
```

### Test Suite

Run the test suite to see example outputs:

```bash
python test_evaluation.py
python test_specific_feedback.py
```

## Components

`config.py`: Configuration and evaluation criteria

- `evaluation.py`: Core evaluation logic
- `specific_feedback.py`: Detailed feedback generation
- `test_*.py`: Test suites with examples

## Evaluation Criteria

The system evaluates theses against:

1. 7 guided reflection criteria
2. 8 common pitfalls

Each criterion checks for specific aspects like:

- Substance and precision
- Scope appropriateness
- Evidence support
- Clarity of claims
- Conciseness

## Output Format

Feedback is provided as a checklist:

```
- [ ] Change: <what needs to change>
  From: <current text>
  To: <suggested revision>
  Why: <explanation>
```

## Limitations

- Requires valid Google AI API key
- Response times vary with API load
- Best for academic/research theses

## Contributing

1. Fork repository
2. Create feature branch
3. Submit pull request

## License

MIT License