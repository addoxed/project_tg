from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

class Keyboard:
    def __init__(self):
        pass

    def _language(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="Русский 🇷🇺", callback_data='l_ru')
        builder.button(text="English 🇺🇸", callback_data='l_en')
        return builder.as_markup()
    
    def _school(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="Schools 🎓", switch_inline_query_current_chat='schools')
        return builder.as_markup()