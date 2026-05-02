import os
from sqladmin import BaseView, expose
from sqlmodel import select
from sqlalchemy import func
from starlette.responses import HTMLResponse
from datetime import datetime, timedelta

from app.models.users import User
from app.database import async_session


class Stats(BaseView):
    name = "Статистика"
    icon = "fa-solid fa-chart-line"

    @expose("/stats", methods=["GET"])
    async def stats_page(self, request):
        async with async_session() as session:
            period = request.query_params.get("period")

            if period == "7":
                start_date = datetime.now() - timedelta(days=7)
            elif period == "30":
                start_date = datetime.now() - timedelta(days=30)
            else:
                start_date = None

            if start_date:
                total_result = await session.exec(
                    select(func.count(User.id)).where(User.created_at >= start_date)
                  )
            else:
                total_result = await session.exec(select(func.count(User.id)))
            total_users = total_result.one()


            query = select(func.date(User.created_at), func.count(User.id)).group_by(func.date(User.created_at)).order_by(func.date(User.created_at))
            if start_date:
                query = query.where(User.created_at >= start_date)
            dates_result = await session.exec(query)
            by_dates = dates_result.all()

            
            if start_date:
                weight_loss_count = await session.exec(
                    select(func.count(User.id)).where(User.weight_loss == True, User.created_at >= start_date)
                  )
                improvement_count = await session.exec(
                      select(func.count(User.id)).where(User.improve_ment == True, User.created_at >= start_date)
                  )
                mode_count = await session.exec(
                      select(func.count(User.id)).where(User.mode == True, User.created_at >= start_date)
                  )
            else:
                weight_loss_count = await session.exec(
                    select(func.count(User.id)).where(User.weight_loss == True)
                  )
                improvement_count = await session.exec(
                    select(func.count(User.id)).where(User.improve_ment == True)
                  )
                mode_count = await session.exec(
                    select(func.count(User.id)).where(User.mode == True)
                  )

            goals = {
                  "weight_loss": weight_loss_count.one() or 0,
                  "improvement": improvement_count.one() or 0,
                  "mode": mode_count.one() or 0
              }

            
            by_dates_list = [{"date": str(row[0]), "count": row[1]} for row in by_dates]

            
            
            template_path = os.path.join(os.path.dirname(__file__), "templates", "stats.html")
            with open(template_path, "r", encoding="utf-8") as f:
                  html_content = f.read()

            
            html_content = html_content.replace("{{ total_users }}", str(total_users))
            html_content = html_content.replace("{{ goals.weight_loss }}", str(goals["weight_loss"]))
            html_content = html_content.replace("{{ goals.improvement }}", str(goals["improvement"]))
            html_content = html_content.replace("{{ goals.mode }}", str(goals["mode"]))
            html_content = html_content.replace("{{ by_dates | safe }}", str(by_dates_list))

            return HTMLResponse(content=html_content)