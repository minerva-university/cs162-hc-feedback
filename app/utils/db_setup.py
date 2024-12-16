import json
from app.models import db, Cornerstone, HC, GuidedReflection, CommonPitfall

def init_db():
    db.drop_all()
    db.create_all()

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def populate_db(json_data):
    # Create cornerstones
    cornerstones = {}
    for cornerstone_name, hcs_data in json_data.items():
        cornerstone = Cornerstone(name=cornerstone_name)
        db.session.add(cornerstone)
        cornerstones[cornerstone_name] = cornerstone

    db.session.commit()

    # Create HCs and their related data
    for cornerstone_name, hcs_data in json_data.items():
        cornerstone = cornerstones[cornerstone_name]

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

def setup_database(json_file_path):
    init_db()
    json_data = load_json_data(json_file_path)
    populate_db(json_data)
