# Import necessary modules
from .db import db
from .models import HCDescription

# Create instances of HCDescription for each HC
hc_composition = HCDescription(
    HC_name="Composition",
    short_desc="Communicate with a clear and precise style.",
    paragraph_desc=(
        "Effective communication requires a clear and precise style that reflects the voice of the communicator and is appropriate "
        "for the intended audience. Communicators should use the fewest words necessary (respecting the principle of 'parsimony') "
        "and carefully select words to ensure clarity and facilitate transitions between ideas. Avoid passive voice, stilted diction, "
        "elaborate structure, and imprecision; write and speak simply, directly, and sincerely. Understand when to use paraphrase, quotation, "
        "or summary to incorporate necessary information smoothly into your communication. Understanding of the learning outcome is evident "
        "through clear, well-justified work at an appropriate level of depth. There are no remaining gaps, errors, or flaws relevant to the application. "
        "The work is strong enough to be used as an exemplar in the course."
    ),
    course="CS",  # Course category
    application_example=(
        "Compose a research proposal with clear objectives and structure, ensuring the language is precise and the arguments are logical. "
        "An exemplary composition will communicate ideas effectively to both technical and non-technical audiences."
    ),
)

hc_audience = HCDescription(
    HC_name="Audience",
    short_desc="Tailor oral and written work by considering the audience.",
    paragraph_desc=(
        "Different audiences have different background knowledge, interests, goals, worldviews, and perspectives. To communicate effectively, "
        "one must recognize these characteristics and tailor messages accordingly. When an audience consists of people with varying levels of "
        "knowledge, goals, interests, or motivations, it is not possible to reach all of them equally effectively with the same delivery. "
        "Learning about and carefully considering an audience’s point of view can help design communications that they can grasp, appeal to their "
        "interests, and perceive as compelling."
    ),
    course="AH",  # Course category
    application_example=(
        "Deliver a persuasive speech tailored to a diverse audience, addressing their varying perspectives and interests. "
        "An exemplary speech will demonstrate a deep understanding of the audience and achieve a compelling delivery."
    ),
)

# Add the instances to the session
db.session.add(hc_composition)
db.session.add(hc_audience)

# Commit the session to save the data
db.session.commit()

print("HC descriptions for 'Composition' and 'Audience' have been successfully added.")
