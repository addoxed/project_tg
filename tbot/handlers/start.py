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
from tbot.utils.states import SignUp, Menu
from tbot.keyboards import inline
from tools.from_json import from_json

class Start:
    def __init__(self):
        self.router = Router()
        self.users = Users()
        self.inline_kb = inline.Keyboard()
        self.SignUp, self.Menu = SignUp, Menu

        self.register_handlers()

    def register_handlers(self):
        
        @self.router.message(Command("start"))
        async def __start(message: Message, state: FSMContext):
            if not self.users._exists(message.from_user.id):
                await message.answer("Привет! Выбери язык.\n\nHi! Choose a language.", reply_markup=self.inline_kb._language())
            
            else:
                pattern = {
                    "ru": f"Привет! Давно не виделись, {self.users._name(message.from_user.id)}.\n\nДоступное меню:",
                    "en": f"Hi! Been a while, {self.users._name(message.from_user.id)}.\n\nAvailable menu:"
                }
                await message.answer(pattern[self.users._user_lang(message.from_user.id)], reply_markup=self.inline_kb._menu())
                await state.set_state(self.Menu)


        @self.router.callback_query(F.data.startswith('l_'))
        async def __new(callback: CallbackQuery, state: FSMContext):
            language = callback.data[2:]
            await state.update_data(language=language)
            pattern = {
                "ru": "Как к тебе обращаться?", 
                "en": "What's your name?"
            }
            await state.set_state(self.SignUp.name)
            await callback.message.answer((pattern[language]))

        
        @self.router.message(self.SignUp.name)
        async def __name(message: Message, state: FSMContext):
            name = message.text
            lang = (await state.get_data())["language"]
            
            if not name.isalpha() and not (2 <= len(name) <= 15):
                pattern = {
                    "ru": "Слишком длинное или недопустимое имя.", 
                    "en": "The name is too long or invalid."
                }
                await message.answer(pattern[lang])
                return
            
            await state.update_data(name=name)
            pattern = {
                "ru": "Сколько тебе лет?", 
                "en": "How old are you?"
            }
            await message.answer(pattern[lang])
            await state.set_state(self.SignUp.age) 

        
        @self.router.message(self.SignUp.age)
        async def __age(message: Message, state: FSMContext):
            age = message.text
            lang = (await state.get_data())["language"]
            if not age.isdigit() or (age.isdigit() and not 17 <= int(age) <= 25):
                pattern = {
                    "ru": "Недопустимое значение возраста.",
                    "en": "Invalid age value."
                }
                await message.answer(pattern[lang])
                return

            await state.update_data(age=int(age))
            pattern = {
                "ru": "Выбери свою школу.",
                "en": "Choose your school."
            }
            await message.answer(pattern[lang], reply_markup=self.inline_kb._school())
            await state.set_state(self.SignUp.school)
        
        
        @self.router.inline_query(self.SignUp.school, F.query == "schools")
        async def __school(iquery: InlineQuery, state: FSMContext):
            lang = (await state.get_data())["language"]
            results = []
            
            for item in from_json.get_schools(lang):
                results.append(
                    InlineQueryResultArticle(
                        id = f"{item["id"]}",
                        title = f"{item["id"]}. " + item["title"],
                        description = item["description"],
                        thumbnail_url=item["url"],
                        input_message_content=InputTextMessageContent(
                            message_text=f"{item["id"]}. " + item["title"]
                        )
                    )
                )
            
            await iquery.answer(results, is_personal=True)
        
        
        @self.router.message(self.SignUp.school)
        async def __chosenschool(message: Message, state: FSMContext):
            data = await state.get_data()
            language, name, age = data["language"], data["name"], data["age"]
            school_id = int((message.text.split(". "))[0])
            await state.clear()

            pattern = {
                "ru": "Успешная регистрация.\n\nДоступное меню:", 
                "en": "Successfull signup.\n\nAvailable menu:"
            }
            self.users._signup(message.from_user.id, language, name, age, school_id)
            await message.answer(f"{name}! {pattern[language]}",
                reply_markup=self.inline_kb._menu()
            )
            await state.set_state(self.Menu)


