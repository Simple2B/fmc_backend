from sqladmin import ModelView

from app.model import Coach


class CoachAdmin(ModelView, model=Coach):
    """Class for setting up the Admin panel for the User model"""

    # Permission
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # Metadata
    name = "Coach"
    name_plural = "Coaches"
    icon = "fa-solid fa-user"

    column_list = [Coach.id, Coach.email]
    column_searchable_list = [Coach.email]
    column_sortable_list = [Coach.id, Coach.email]

    # Details
    column_details_list = [Coach.id, Coach.email]

    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]
