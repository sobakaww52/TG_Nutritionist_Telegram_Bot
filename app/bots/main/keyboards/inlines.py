from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(
        text="📝 Создать анкету", 
        callback_data="start_registration")
    )
    
    return builder.as_markup()