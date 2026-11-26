import random
import sys

from app.database import Base, SessionLocal, engine
from app.models import Court

Base.metadata.create_all(bind=engine)

COURT_TYPES = ["tennis", "pickleball", "basketball", "volleyball", "badminton"]
STREET_NAMES = [
    "River St",
    "Fawcett St",
    "Union Sq",
    "Washington St",
    "Columbia Rd",
    "Beacon St",
    "Main St",
    "Highland Ave",
    "Elm St",
    "Oak Ave",
]
CITIES = [
    ("Boston", "MA", "02136"),
    ("Cambridge", "MA", "02138"),
    ("Somerville", "MA", "02143"),
    ("Brookline", "MA", "02445"),
    ("Dorchester", "MA", "02125"),
    ("Medford", "MA", "02155"),
    ("Quincy", "MA", "02169"),
    ("Newton", "MA", "02458"),
]
HOURS_OPTIONS = [
    "Mon-Sun 6am-10pm",
    "Mon-Fri 7am-9pm, Sat-Sun 8am-8pm",
    "Mon-Sun 6am-11pm",
    "Mon-Sun 6am-9pm",
    "Mon-Sun 7am-9pm",
]


def random_court(index):
    city, state, zipcode = random.choice(CITIES)
    court_type = random.choice(COURT_TYPES)
    return {
        "name": f"{city} {court_type.capitalize()} Court {index}",
        "type": court_type,
        "address_1": f"{random.randint(1, 999)} {random.choice(STREET_NAMES)}",
        "address_2": None,
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "image": f"https://picsum.photos/seed/rally-court-{index}/400/300",
        "hours_of_operation": random.choice(HOURS_OPTIONS),
    }

SAMPLE_COURTS = [
    {
        "name": "Hyde Park Tennis Courts",
        "type": "tennis",
        "address_1": "1179 River St",
        "address_2": None,
        "city": "Boston",
        "state": "MA",
        "zipcode": "02136",
        "image": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8",
        "hours_of_operation": "Mon-Sun 6am-10pm",
    },
    {
        "name": "Cambridge Pickleball Center",
        "type": "pickleball",
        "address_1": "75 Fawcett St",
        "address_2": "Suite B",
        "city": "Cambridge",
        "state": "MA",
        "zipcode": "02138",
        "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea",
        "hours_of_operation": "Mon-Fri 7am-9pm, Sat-Sun 8am-8pm",
    },
    {
        "name": "Somerville Community Basketball Court",
        "type": "basketball",
        "address_1": "90 Union Sq",
        "address_2": None,
        "city": "Somerville",
        "state": "MA",
        "zipcode": "02143",
        "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc",
        "hours_of_operation": "Mon-Sun 6am-11pm",
    },
    {
        "name": "Brookline Tennis & Pickleball Club",
        "type": "tennis",
        "address_1": "375 Washington St",
        "address_2": None,
        "city": "Brookline",
        "state": "MA",
        "zipcode": "02445",
        "image": "https://images.unsplash.com/photo-1599586120429-48281b6f0ece",
        "hours_of_operation": "Mon-Sun 6am-9pm",
    },
    {
        "name": "Dorchester Pickleball Courts",
        "type": "pickleball",
        "address_1": "500 Columbia Rd",
        "address_2": None,
        "city": "Dorchester",
        "state": "MA",
        "zipcode": "02125",
        "image": "https://images.unsplash.com/photo-1600965962102-9d260a71890d",
        "hours_of_operation": "Mon-Sun 7am-9pm",
    },
]


def seed(count=None):
    db = SessionLocal()
    try:
        if count is not None:
            existing = db.query(Court).count()
            for i in range(count):
                db.add(Court(**random_court(existing + i + 1)))
            db.commit()
            print(f"Seeded {count} random courts.")
            return

        if db.query(Court).count() > 0:
            print("Courts already seeded, skipping.")
            return

        for court_data in SAMPLE_COURTS:
            db.add(Court(**court_data))
        db.commit()
        print(f"Seeded {len(SAMPLE_COURTS)} courts.")
    finally:
        db.close()


if __name__ == "__main__":
    arg_count = int(sys.argv[1]) if len(sys.argv) > 1 else None
    seed(arg_count)
