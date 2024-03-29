from invoke import task
from faker import Faker
from pydantic import BaseModel

from app.logger import log
from app.config import Settings, get_settings
from app.database import get_db, Session
import app.model as m


db: Session = get_db().__next__()
settings: Settings = get_settings()
fake = Faker()
SPORTS: list[m.SportType] = db.query(m.SportType).all()


class RealCoach(BaseModel):
    first_name: str
    last_name: str
    email: str
    profile_picture: str
    sport: str
    city: str
    postal_code: str


class RealCoachList(BaseModel):
    coaches: list[RealCoach]


@task
def create_real_coaches_data(_):
    coaches_data = RealCoachList.parse_file("app/assets/coaches/data.json")
    for data in coaches_data.coaches:
        if not db.query(m.Coach).filter_by(email=data.email).first():
            coach = m.Coach(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                username=data.email,
                profile_picture=data.profile_picture,
                password_hash=data.email,
            )
            db.add(coach)
            db.flush()
            if (
                not db.query(m.Location)
                .filter(m.Location.city.ilike(f"{data.city}"))
                .first()
            ):
                location = m.Location(
                    city=data.city,
                    street=fake.street_name(),
                    postal_code=data.postal_code,
                )
                db.add(location)
                db.flush()
                coach_location = m.CoachLocation(
                    location_id=location.id, coach_id=coach.id
                )
                db.add(coach_location)
                db.flush()
            sport = (
                db.query(m.SportType)
                .filter(m.SportType.name.ilike(f"{data.sport}"))
                .first()
            )
            if not sport:
                sport = m.SportType(name=data.sport)
                db.add(sport)
                db.flush()
                db.refresh(sport)
            if not (
                db.query(m.CoachSport)
                .filter_by(coach_id=coach.id, sport_id=sport.id)
                .first()
            ):
                db.add(m.CoachSport(coach_id=coach.id, sport_id=sport.id))

        db.commit()
        log(log.INFO, "Coach %s %s created", coach.first_name, coach.last_name)
