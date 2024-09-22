import json
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, 
    CallbackQuery, 
    InlineQuery, 
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    ChosenInlineResult
)

from db.collections.users import Users
from tbot.utils.states import SignUp
from tbot.keyboards import inline

class Starts:
    def __init__(self):
        self.router = Router()
        self.users = Users()
        self.inline_kb = inline.Keyboard()
        self.SignUp = SignUp

       

        self.register_handlers()

    def get_schools(self, lang: str):
        with open('src/schools.json', 'r', encoding='utf-8') as f:
            return json.load(f)[lang]

    def register_handlers(self):
        
        @self.router.message(Command("start"))
        async def __start(message: Message):
            if not self.users._exists(message.from_user.id):
                await message.answer("Привет! Выбери язык.\n\nHi! Choose a language.", reply_markup=self.inline_kb._language())


        @self.router.callback_query(F.data.startswith('l_'))
        async def __new(callback: CallbackQuery, state: FSMContext):
            uid, lang = callback.from_user.id, callback.data[2:]
            self.users._new(uid, lang) 
            pattern = {
                "ru": "Как к тебе обращаться?", 
                "en": "What's your name?"
            }
            await state.set_state(self.SignUp.name)
            await callback.message.answer((pattern[lang]))

        
        @self.router.message(self.SignUp.name)
        async def __name(message: Message, state: FSMContext):
            name = message.text
            if not name.isalpha() and not (2 <= len(name) <= 15):
                pattern = {
                    "ru": "Слишком длинное или недопустимое имя.", 
                    "en": "The name is too long or invalid."
                }
                await message.answer(pattern[self.users.user_lang(message.from_user.id)])
                return
            
            await state.update_data(name=name)
            pattern = {
                "ru": "Сколько тебе лет?", 
                "en": "How old are you?"
            }
            await message.answer(pattern[self.users.user_lang(message.from_user.id)])
            await state.set_state(self.SignUp.age) 

        
        @self.router.message(self.SignUp.age)
        async def __age(message: Message, state: FSMContext):
            age = message.text
            if not age.isdigit() or (age.isdigit() and not 17 <= int(age) <= 25):
                pattern = {
                    "ru": "Недопустимое значение возраста.",
                    "en": "Invalid age value."
                }
                await message.answer(pattern[self.users.user_lang(message.from_user.id)])
                return

            await state.update_data(age=int(age))
            pattern = {
                "ru": "Выбери свою школу.",
                "en": "Choose your school."
            }
            await message.answer(pattern[self.users.user_lang(message.from_user.id)], reply_markup=self.inline_kb._school())
            await state.set_state(self.SignUp.school)
        
        
        @self.router.inline_query(self.SignUp.school, F.query == "schools")
        async def __school(iquery: InlineQuery, state: FSMContext):
            results = []

            for item in self.get_schools(self.users.user_lang(iquery.from_user.id)):
                results.append(
                    InlineQueryResultArticle(
                        id = item["title"],
                        title = item["title"],
                        description = item["description"],
                        thumbnail_url=item["url"],
                        input_message_content=InputTextMessageContent(
                            message_text=item["title"]
                        )
                    )
                )
            
            await iquery.answer(results, is_personal=True)
        
        
        @self.router.message(self.SignUp.school)
        async def __chosenschool(message: Message, state: FSMContext):
            data = await state.get_data()
            name, age, school = data["name"], data["age"], message.text

            self.users._signedup(message.from_user.id, name, age, school)
            await message.answer(f"{name}, {age}, {school}")
            await state.clear()


