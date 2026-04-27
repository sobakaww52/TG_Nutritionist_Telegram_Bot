from aiogram import types, F
from aiogram.fsm.context import FSMContext


async def clean_chat(event: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(event, types.CallbackQuery):
        try:
            await event.answer()
        except Exception: pass
        return True

    try:
        await event.delete()
    except Exception: pass

    if not event.text:
        data = await state.get_data()
        last_msg_id = data.get("last_msg_id")
        
        sent_msg = await event.answer("Пожалуйста, отправьте ваш ответ текстом. Медиа-файлы не поддерживаются. 🙏")
        
        if last_msg_id:
            try:
                await event.bot.delete_message(event.chat.id, last_msg_id)
            except Exception: pass
        
        await state.update_data(last_msg_id=sent_msg.message_id)
        return False

    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    if last_msg_id:
        try:
            await event.bot.delete_message(event.chat.id, last_msg_id)
        except Exception: pass
    return True