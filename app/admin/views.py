import asyncio
from sqladmin import ModelView, action
from sqlmodel import select
from starlette.requests import Request
from starlette.responses import Response
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import InputMediaPhoto, InputMediaVideo
from uuid import UUID

from app.models.users import User, Improvement, Weightloss, Modes
from app.models.broadcasts import Broadcast

from app.bot_instance import bot

class BroadcastAdmin(ModelView, model=Broadcast):
    column_list = [Broadcast.created_at, Broadcast.media_type, Broadcast.is_sent]
    name = "Рассылка"
    name_plural = "Рассылки"
    icon = "fa-solid fa-bullhorn"

    @action(
        name="run_broadcast",
        label="🚀 ЗАПУСТИТЬ",
        confirmation_message="Начать отправку всем пользователям?",
        add_in_detail=True,
        add_in_list=True,
    )
    async def send_broadcast(self, request: Request):
        
        pks = request.query_params.get("pks", "").split(",")
        if not pks or pks == ['']:
            return Response("Сначала выберите запись!", status_code=400)
        try:
            broadcast_id = UUID(pks[0])
        except ValueError:
            return Response("Ошибка: неверный формат ID", status_code=400)
        
        async with self.session_maker() as session:
            
            broadcast = await session.get(Broadcast, broadcast_id)
            if not broadcast or broadcast.is_sent:
                return Response("Рассылка уже была отправлена или не существует")

            users_stmt = select(User.telegram_id)
            users_result = await session.execute(users_stmt)
            user_ids = users_result.scalars().all()

            file_ids = [fid.strip() for fid in broadcast.file_id.split(",")] if broadcast.file_id else []

            count = 0
            for uid in user_ids:
                try:
                    if len(file_ids) > 1:
                        media_group = []
                        for i, fid in enumerate(file_ids):
                            caption = broadcast.text if i == 0 else None
                            
                            if broadcast.media_type == "photo":
                                media_group.append(InputMediaPhoto(media=fid, caption=caption))
                            elif broadcast.media_type == "video":
                                media_group.append(InputMediaVideo(media=fid, caption=caption))
                        
                        await bot.send_media_group(uid, media=media_group)

                    else:
                        current_fid = file_ids[0] if file_ids else None
                        
                        if broadcast.media_type == "photo":
                            await bot.send_photo(uid, photo=current_fid, caption=broadcast.text)
                        elif broadcast.media_type == "video":
                            await bot.send_video(uid, video=current_fid, caption=broadcast.text)
                        else:
                            await bot.send_message(uid, text=broadcast.text)
                    
                    count += 1
                    await asyncio.sleep(0.05)
                
                except TelegramForbiddenError:
                    continue 
                except TelegramRetryAfter as e:
                    await asyncio.sleep(e.retry_after)
                except Exception as e:
                    print(f"Ошибка на {uid}: {e}")

            broadcast.is_sent = True
            await session.commit()

        return Response(f"Успешно! Отправлено: {count} чел.")



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
