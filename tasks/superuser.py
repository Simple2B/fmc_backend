from invoke import task

from app.database import get_db
import app.model as m

db = get_db().__next__()


@task
def create_super_user(_):
    ADMIN_EMAIL = "admin"
    ADMIN_PASSWORD = "admin"
    if not db.query(m.SuperUser).filter_by(email=ADMIN_EMAIL).first():
        su = m.SuperUser(
            username=ADMIN_EMAIL, email=ADMIN_EMAIL, password=ADMIN_PASSWORD
        )
        db.add(su)
        db.commit()
        print("SuperUser created successfully")
