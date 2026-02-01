from aiogram.fsm.state import StatesGroup, State

class HairTest(StatesGroup):
    form = State()
    thickness = State()
    density = State()
    scalp = State()
    length = State()
    porosity = State()
    damage = State()
    age = State()
    result = State()

