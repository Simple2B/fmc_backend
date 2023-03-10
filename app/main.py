# flake8: noqa F402

import jinja2

jinja2.contextfunction = jinja2.pass_context
from starlette.responses import RedirectResponse
from sqlalchemy.engine import Engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.router import router
from app import admin
from app.database import Engine, get_engine


app = FastAPI()
engine: Engine = get_engine()

# admin
sql_admin = Admin(app, engine)
sql_admin.add_view(admin.coach.CoachAdmin)

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# router
app.include_router(router)


@app.get("/", tags=["Docs"])
async def root():
    """Redirect to documentation"""
    return RedirectResponse(url="/docs")
