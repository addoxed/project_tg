from aiogram.fsm.state import StatesGroup, State

class SignUp(StatesGroup):
    name = State()
    age = State()
    school = State()
    end = State()


class Menu(State):
    pass