import os

import google.generativeai as genai

# Thesis evaluation criteria
GUIDED_REFLECTION_CRITERIA = [
    "Is it substantial, precise, relevant, arguable, concise, and sets up evidence?",
    "Is it appropriate in scope?",
    "Is it supported by evidence?",
    "Does it reference types of evidence?",
    "Is it a one to two sentence statement?",
]

# Common thesis pitfalls
COMMON_PITFALLS = [
    "Too vague/open-ended",
    "Too long/too many topics",
    "No clear stance",
    "Claim without reasoning. For example, the thesis says A is B but does not mention A is B because of X, Y, and Z.",
    "Missing importance",
    "Unclear statement",
    "Undefined main points",
    "Scope mismatch",
]


def get_criteria():
    print("[DEBUG] Fetching evaluation criteria")
    return GUIDED_REFLECTION_CRITERIA


def get_pitfalls():
    print("[DEBUG] Fetching common pitfalls")
    return COMMON_PITFALLS


def initialize_evaluation_model():
    """Initialize model optimized for Pass/Fail evaluation"""
    try:
        print("[DEBUG] Configuring evaluation model")
        api_key = "AIzaSyBqj7l0AIxQ78bzg_LYwwsBOoIM7lWMSFY"
        print(f"[DEBUG] API Key present: {bool(api_key)}")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                max_output_tokens=1,  # Minimal tokens for Pass/Fail
            ),
        )
        print("[DEBUG] Evaluation model initialized successfully")
        return model
    except Exception as e:
        print(f"[DEBUG] Error initializing evaluation model: {e}")
        return None


def initialize_analysis_model():
    """Initialize model for detailed analysis"""
    try:
        print("[DEBUG] Configuring analysis model")
        api_key = "AIzaSyBqj7l0AIxQ78bzg_LYwwsBOoIM7lWMSFY"
        print(f"[DEBUG] API Key present: {bool(api_key)}")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=1.0,
                max_output_tokens=10000,  # Higher tokens for detailed analysis
            ),
        )
        print("[DEBUG] Analysis model initialized successfully")
        return model
    except Exception as e:
        print(f"[DEBUG] Error initializing analysis model: {e}")
        return None
