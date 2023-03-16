from invoke import task
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, Session
import app.model as m

db: Session = get_db().__next__()

SPORTS: list[m.SportType] = db.query(m.SportType).all()


def create_footbal_coach():
    FOOTBALL_COACH_EMAIL = "mourinho@gmail.com"
    football_coach = db.query(m.Coach).filter_by(email=FOOTBALL_COACH_EMAIL).first()
    if not football_coach:
        football_coach = m.Coach(
            first_name="Jose",
            last_name="Mourinho",
            username="FootballCoach",
            email=FOOTBALL_COACH_EMAIL,
            password="password",
            is_verified=True,
        )
        db.add(football_coach)
        db.commit()
        fc_sport = m.CoachSport(coach_id=football_coach.id, sport_id=SPORTS[0].id)
        db.add(fc_sport)
        db.commit()
        # TODO create schedule
        print(f"Coach {football_coach} created successfully")
    return football_coach


def create_boxing_coach():
    BOXING_COACH_EMAIL = "tyson@gmail.com"
    boxing_coach = db.query(m.Coach).filter_by(email=BOXING_COACH_EMAIL).first()
    if not boxing_coach:
        boxing_coach = m.Coach(
            first_name="Michael",
            last_name="Tyson",
            username="BoxingCoach",
            email=BOXING_COACH_EMAIL,
            password="password",
            is_verified=True,
        )
        db.add(boxing_coach)
        db.commit()
        bc_sport = m.CoachSport(coach_id=boxing_coach.id, sport_id=SPORTS[7].id)
        db.add(bc_sport)
        db.commit()
        print(f"Coach {boxing_coach} created successfully")
    # TODO create schedule
    return db.query(m.Coach).filter_by(email=BOXING_COACH_EMAIL).first()


def create_dummy_locations():
    locations = db.query(m.Location).all()
    if not locations:
        locations = [
            m.Location(
                name="São Paulo Sport Hall",
                address_line_1="Rua São Paulo",
                address_line_2="123",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall",
                address_line_1="Rua São Paulo",
                address_line_2="124",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall #2",
                address_line_1="Rua São Paulo",
                address_line_2="125",
            ),
            m.Location(
                name="Rio de Janeiro Sport Hall #3",
                address_line_1="Rua São Paulo",
                address_line_2="126",
            ),
        ]
        db.add_all(locations)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
        print("Locations created successfully")
    return locations


def create_dummy_students():
    students = db.query(m.Student).all()
    if not students:
        students = [
            m.Student(
                first_name="John",
                last_name="Doe",
                username="johndoe",
                email="johndoe@gmail.com",
                password="password",
                is_verified=True,
            ),
            m.Student(
                first_name="Jane",
                last_name="Doe",
                username="janedoe",
                email="janedoe@gmail.com",
                password="password",
                is_verified=True,
            ),
        ]
        db.add_all(students)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
        print("Students created successfully")
    return students


@task
def dummy_data(_):
    create_footbal_coach()
    create_boxing_coach()
    # create_dummy_locations()
    create_dummy_students()

    # todo create lessons
