from invoke import task

from app.database import get_db
import app.model as m

SPORTS_TYPES = [
    "Football",
    "Cricket",
    "Tennis",
    "Yoga",
    "Rugby",
    "Fitness",
    "Golf",
    "Swimming",
    "Boxing",
]

db = get_db().__next__()


@task
def create_sports(_):
    for s in SPORTS_TYPES:
        sport = db.query(m.SportType).filter_by(name=s).first()
        if not sport:
            print(f"Creating a new sport - {s}")
            new_sport = m.SportType(name=s)
            db.add(new_sport)
            db.commit()
        else:
            print(f"{sport} already exists")
