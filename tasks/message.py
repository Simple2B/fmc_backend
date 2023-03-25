from invoke import task


from app.database import get_db, Session
import app.model as m


db: Session = get_db().__next__()


@task
def get_coaches(_):
    coaches: list[m.Coach] = db.query(m.Coach).all()
    for coach in coaches:
        print(f"Coach:\n\t{coach.uuid}\t{coach.email}\n")


@task
def get_students(_):
    students = db.query(m.Student).all()
    for student in students:
        print(f"Student:\n\t{student.uuid}\t{student.email}\n")


@task
def message_to_coach(_, author: str, receiver: str, text: str = "Hello"):
    """Create message from someone to somebody"""
    # TODO
    student = db.query(m.Student).filter_by(email=author).first()
    coach = db.query(m.Coach).filter_by(email=receiver).first()

    if not coach or not student:
        print("Author or receiver not found")
        exit()
    text = f"Message from {student} to {coach}:{text} has been sent"
    db.add(m.Message(author_id=student.uuid, receiver_id=coach.uuid, text=text))
    db.commit()
    print(f"Message from {student} to {coach}:{text} has been sent")


@task
def message_to_student(_, author: str, receiver: str, text: str = "Hello"):
    """Create message from someone to somebody"""
    # TODO
    student = db.query(m.Student).filter_by(email=receiver).first()
    coach = db.query(m.Coach).filter_by(email=author).first()

    if not coach or not student:
        print("Author or receiver not found")
        exit()
    text = f"Message from {coach} to {student}:{text} has been sent"
    db.add(m.Message(author_id=coach.uuid, receiver_id=student.uuid, text=text))
    db.commit()
    print(f"Message from {coach} to {student}:{text} has been sent")
