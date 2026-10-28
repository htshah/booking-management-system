from app.database import Base, SessionLocal, engine
from app.models import Court

Base.metadata.create_all(bind=engine)

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


def seed():
    db = SessionLocal()
    try:
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
    seed()
