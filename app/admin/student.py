from sqladmin import ModelView

from app.model import Student


class StudentAdmin(ModelView, model=Student):
    """Class for setting up the Admin panel for the User model"""

    # Permission
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # Metadata
    name = "Student"
    name_plural = "Students"
    icon = "fa-solid fa-user"

    column_list = [Student.id, Student.email]
    column_searchable_list = [Student.email]
    column_sortable_list = [Student.id, Student.email]

    # Details
    column_details_list = [Student.id, Student.email]

    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]
