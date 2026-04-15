from sqladmin import Admin, ModelView

from app.models.users import User


class UserAdmin(ModelView, model=User):
    column_list=[User.id, User.first_name, User.tg_username, User.age, User.height, User.weight]
    column_searchable_list = [User.tg_username]
    name = "Нового клиента"
    name_plural = "БАЗА КЛИЕНТОВ"
    icon = "fa-solid fa-user"

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)