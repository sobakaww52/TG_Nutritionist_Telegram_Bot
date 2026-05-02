from sqladmin import Admin
from app.admin.views import UserAdmin, ImproveAdmin, WeightLossAdmin, ModesAdmin, BroadcastAdmin
from app.admin.auth import authentication_backend
from app.admin.stats import Stats

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

    admin.add_view(BroadcastAdmin)

    admin.add_view(Stats)