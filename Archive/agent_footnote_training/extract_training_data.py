from app import create_app
from app.models import HC, Cornerstone
import json
from pathlib import Path

def extract_hc_pairs():
    # Initialize app context
    app = create_app()

    with app.app_context():
        # Query all HCs
        hcs = HC.query.all()

        # Create paired data
        training_pairs = [
            {
                "cornerstone": hc.cornerstone.name,
                "general_example": hc.general_example,
                "footnote": hc.footnote
            }
            for hc in hcs
        ]

        # Save to JSON file
        output_path = Path(__file__).parent / "training_data.json"
        with open(output_path, "w") as f:
            json.dump(
                {
                    "training_pairs": training_pairs,
                    "total_pairs": len(training_pairs)
                },
                f,
                indent=2
            )

        print(f"Extracted {len(training_pairs)} training pairs to {output_path}")
        return training_pairs

if __name__ == "__main__":
    extract_hc_pairs()