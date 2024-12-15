import json
from pathlib import Path
from .models import db, Cornerstone, HC, GuidedReflection, CommonPitfall

def init_db():
    """Create all database tables"""
    db.create_all()

def populate_data():
    """Populate database with initial data from local JSON file"""
    json_path = Path(__file__).parent / 'data' / 'hcs.json'

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        for cornerstone_name, hcs_data in data.items():
            # Create cornerstone
            cornerstone = Cornerstone(name=cornerstone_name)
            db.session.add(cornerstone)
            db.session.commit()

            # Add HCs for this cornerstone
            for hc_data in hcs_data:
                hc = HC(
                    name=hc_data['hc_name'],
                    footnote=hc_data['footnote'],
                    general_example=hc_data['general_example'],
                    cornerstone=cornerstone
                )
                db.session.add(hc)

                # Add guided reflections
                for reflection in hc_data['guided_reflection']:
                    gr = GuidedReflection(text=reflection, hc=hc)
                    db.session.add(gr)

                # Add common pitfalls
                for pitfall in hc_data['common_pitfalls']:
                    cp = CommonPitfall(text=pitfall, hc=hc)
                    db.session.add(cp)

            db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
