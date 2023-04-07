# flake8: noqa F402

import jinja2


jinja2.contextfunction = jinja2.pass_context
from starlette.responses import RedirectResponse
from sqlalchemy.engine import Engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin import authentication_backend
from app.router import router
from app import admin
from app.database import Engine, get_engine
from app.utils import custom_generate_unique_id


app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
engine: Engine = get_engine()

# admin
sql_admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
    templates_dir="app/templates/admin",
)
admin_views = (admin.CoachAdmin, admin.StudentAdmin)
for view in admin_views:
    sql_admin.add_view(view)


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
