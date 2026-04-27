from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📝 Создать анкету", callback_data="start_registration"),
        InlineKeyboardButton(text="👤 Моя анкета", callback_data="my_profile")
    )
    

    return builder.as_markup()

def get_finish_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="Похудеть", callback_data="gets_loss"))
    builder.row(InlineKeyboardButton(text="Улучшить самочувствие", callback_data="gets_improve"))
    builder.row(InlineKeyboardButton(text="Наладить режим", callback_data="gets_mode"))
    
    return builder.as_markup()

def how_water_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Не люблю пить воду", callback_data="no_water"))
    builder.row(InlineKeyboardButton(text="Воду пью, но не контролирую", callback_data="mb_water"))
    builder.row(InlineKeyboardButton(text="Воду пью и контролирую", callback_data="like_water"))

    return builder.as_markup()

def yes_or_not_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Да", callback_data="input_yes"))
    builder.row(InlineKeyboardButton(text="Нет", callback_data="input_no"))

    return builder.as_markup()

def delete_registr() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_fst"),InlineKeyboardButton(text="❌ Удалить анкету", callback_data="delete_profile"))

    return builder.as_markup()