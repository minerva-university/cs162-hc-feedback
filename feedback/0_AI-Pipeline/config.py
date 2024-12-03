import os
import google.generativeai as genai

# Thesis evaluation criteria
GUIDED_REFLECTION_CRITERIA = [
    "Is it substantial, precise, relevant, arguable, concise, and sets up evidence?",
    "Is it appropriate in scope?",
    "Is it supported by evidence?",
    "Does it reference types of evidence?",
    "Is it a one to two sentence statement?"
]

COMMON_PITFALLS = [
    "Too vague/open-ended",
    "Too long/too many topics",
    "No clear stance",
    "Claim without reasoning",
    "Missing importance",
    "Unclear statement",
    "Undefined main points",
    "Scope mismatch"
]

def get_criteria():
    return GUIDED_REFLECTION_CRITERIA

def get_pitfalls():
    return COMMON_PITFALLS

def initialize_evaluation_model():
    """Initialize model optimized for Pass/Fail evaluation"""
    try:
        api_key = "AIzaSyBqj7l0AIxQ78bzg_LYwwsBOoIM7lWMSFY"
        if not api_key:
            raise ValueError("API key not found")

        genai.configure(api_key=api_key)
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                max_output_tokens=1,  # Minimal tokens for Pass/Fail
            ),
        )
    except Exception as e:
        print(f"Error initializing evaluation model: {e}")
        return None

def initialize_analysis_model():
    """Initialize model for detailed analysis"""
    try:
        api_key = "AIzaSyBqj7l0AIxQ78bzg_LYwwsBOoIM7lWMSFY"
        if not api_key:
            raise ValueError("API key not found")

        genai.configure(api_key=api_key)
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                max_output_tokens=10000,  # Higher tokens for detailed analysis
            ),
        )
    except Exception as e:
        print(f"Error initializing analysis model: {e}")
        return None