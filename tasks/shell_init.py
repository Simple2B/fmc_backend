# flake8: noqa F401
from app import model as m
from app.database import get_db

db = get_db().__next__()
