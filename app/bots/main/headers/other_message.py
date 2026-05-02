from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.config import settings

router = Router()

@router.message(F.from_user.id == settings.ADMIN_ID, F.photo)
async def catch_photo_id(message: types.Message):
    file_id = message.photo[-1].file_id
    await message.answer(f"ID ФОТО:\n<code>{file_id}</code>", parse_mode="HTML")

@router.message(F.from_user.id == settings.ADMIN_ID, F.video)
async def catch_video_id(message: types.Message):
    file_id = message.video.file_id
    await message.answer(f"ID ВИДЕО:\n<code>{file_id}</code>", parse_mode="HTML")

@router.message()
async def echo_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        try:
            await message.delete()
        except Exception:
            pass

        content_type = "сообщение"
        if message.video_note:
            content_type = "кружочек"
        elif message.photo:
            content_type = "фотографию"
        elif message.voice:
            content_type = "голосовое сообщение"
        elif message.sticker:
            content_type = "стикер"

        data = await state.get_data()
        last_msg_id = data.get("last_msg_id")
        if last_msg_id:
            try:
                await message.bot.delete_message(message.chat.id, last_msg_id)
            except:
                pass

        sent_msg = await message.answer(
            f"Я увидел ваш {content_type}, но сейчас я принимаю только ответы по теме или через /start. 🙏"
        )
        await state.update_data(last_msg_id=sent_msg.message_id)