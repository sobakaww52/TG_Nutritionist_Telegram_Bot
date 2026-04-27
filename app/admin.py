from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.models.users import User, Improvement, Weightloss, Modes
from app.config import settings

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        
        if username == settings.ADMIN_LOGIN and password == settings.ADMIN_PASSWORD:
            request.session.update({"token": "authenticated"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)




class UserAdmin(ModelView, model=User):
    column_list=[User.telegram_id, User.fio, User.mail, User.tg_username, User.age, User.height, User.weight, User.weight_loss, User.improve_ment, User.mode]
    column_searchable_list = [User.tg_username]
    column_default_sort = [("id", True)]
    name = "Нового клиента"
    name_plural = "БАЗА КЛИЕНТОВ"
    icon = "fa-solid fa-user"

class ImproveAdmin(ModelView, model=Improvement):
    column_list = [Improvement.users_tg ,Improvement.improve_ment, Improvement.tg_username, Improvement.problem]
    name = "Улучшение самочувствия"
    name_plural = "Улучшение самочувствия"
    category = "Из опросников"
    icon = "fa-solid fa-heart-pulse"

class WeightLossAdmin(ModelView, model=Weightloss):
    column_list = [Weightloss.users_tg, Weightloss.weight_loss, Weightloss.tg_username, Weightloss.how_kg, Weightloss.how_eat,
                    Weightloss.how_active, Weightloss.how_water, Weightloss.how_sleep]
    
    name = "Похудение"
    name_plural = "Похудение"
    category = "Из опросников"
    icon = "fa-solid fa-weight-scale"

class ModesAdmin(ModelView, model=Modes):
    column_list = [Modes.users_tg, Modes.mode, Modes.tg_username, Modes.have_kg, Modes.how_eat,
                    Modes.how_active, Modes.how_water, Modes.how_sleep]
    
    name = "Наладить режим"
    name_plural = "Наладить режим"
    category = "Из опросников"
    icon = "fa-solid fa-sliders"


def setup_admin(app, engine):
    admin = Admin(
        app, 
        engine,
        authentication_backend=authentication_backend,
        title="admin panel"
    )
    admin.add_view(UserAdmin)
    admin.add_view(ImproveAdmin)
    admin.add_view(WeightLossAdmin)
    admin.add_view(ModesAdmin)