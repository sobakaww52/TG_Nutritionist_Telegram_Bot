from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(
        text="📝 Создать анкету", 
        callback_data="start_registration")
    )
    
    return builder.as_markup()

def get_finish_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="Похудеть", callback_data="gets_loss"))
    builder.row(InlineKeyboardButton(text="Улучшить самочувствие", callback_data="gets_improve"))
    builder.row(InlineKeyboardButton(text="Наладить режим", callback_data="gets_mode"))
    
    return builder.as_markup()