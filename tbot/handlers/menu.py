from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, 
    CallbackQuery, 
    InlineQuery, 
    InlineQueryResultArticle, 
    InputTextMessageContent
)

from db.collections.users import Users
from tbot.utils.states import Menu
from tbot.keyboards import inline

class BotMenu:
    def __init__(self):
        self.router = Router()
        self.users = Users()
        self.inline_kb = inline.Keyboard()
        self.Menu = Menu

        self.register_handlers()

    def register_handlers(self):
        
        @self.router.callback_query()
        async def __start(callback: CallbackQuery):
            pass