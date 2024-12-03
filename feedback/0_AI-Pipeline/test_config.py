
from config import initialize_evaluation_model, initialize_analysis_model

def main():
    print("Testing Evaluation Model...")
    eval_model = initialize_evaluation_model()
    print(f"Evaluation Model initialized: {eval_model is not None}")

    print("\nTesting Analysis Model...")
    analysis_model = initialize_analysis_model()
    print(f"Analysis Model initialized: {analysis_model is not None}")

if __name__ == "__main__":
    main()