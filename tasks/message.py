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
def send_message(_, author, receiver, text: str = "Hello"):
    # TODO
    coach = db.query(m.Coach).filter_by(uuid=author).first()
    student = db.query(m.Student).filter_by(uuid=receiver).first()
    if not coach or not student:
        print("Author or receiver not found")
        exit()
    if coach:
        author = coach
        receiver = student
    else:
        author = student
        receiver = coach
    db.add(m.Message(author_id=author, receiver_id=receiver, text=text))
    db.commit()
    print(f"Message from {author} to {receiver}:{text} has been sent")
