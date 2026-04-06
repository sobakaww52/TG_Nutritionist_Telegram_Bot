import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.database import init_db

bot = Bot(token=settings.BOT_MAIN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    webhook_url = f"{settings.DOMAIN}/webhook"
    
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )
    
    yield
    
    await bot.delete_webhook()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def bot_webhook(request: Request):

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)