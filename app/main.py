import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Dispatcher, types
from starlette.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db, engine
from app.bots.main.headers.started_router import router as user_router
from app.bots.main.headers.registration import router as registration_router
from app.bots.main.headers.other_message import router as other_massage_router
from app.bots.main.services.show_profile import router as my_profile
from app.bot_instance import bot
from app.admin import setup_admin


dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(registration_router)
dp.include_router(my_profile)
dp.include_router(other_massage_router)



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    webhook_url_main = f"{settings.DOMAIN}/webhook/{settings.BOT_MAIN}"
    
    await bot.set_webhook(
        url=webhook_url_main,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )
    
    yield
    
    await bot.delete_webhook()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)


@app.post("/webhook/{BOT_MAIN}")
async def bot_webhook(request: Request, BOT_MAIN: str):

    update_data = await request.json()
    
    update = types.Update.model_validate(update_data, context={"bot": bot})
    
    await dp.feed_update(bot, update)
    
    return {"ok": True}

@app.get("/")
async def index():
    return {
        "status": "running", 
        "bot_info": "NutriBot is active",
        "domain": settings.DOMAIN
    }

app.mount("/admin/static", StaticFiles(directory="app/admin/static"), name="admin_static")

setup_admin(app, engine)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)