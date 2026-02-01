import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import BOT_TOKEN
from states import HairTest
from questions import QUESTIONS
from logic import apply_corrections
from texts import format_result

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def make_keyboard(options: dict):
    kb = []
    for key, text in options.items():
        kb.append([KeyboardButton(text=text)])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Пройдём короткий тест из 8 вопросов 👇")
    await state.set_state(HairTest.form)

    q = QUESTIONS["form"]
    await message.answer(
        q["text"],
        reply_markup=make_keyboard(q["options"])
    )


@dp.message(HairTest.form)
async def form_step(message: types.Message, state: FSMContext):
    key = get_option_key("form", message.text)

    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(form=key)

    await state.set_state(HairTest.thickness)
    q = QUESTIONS["thickness"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))


# ⚠️ Аналогично добавляются остальные шаги (я могу дописать полностью)

@dp.message(HairTest.age)
async def finish(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    data = apply_corrections(data)
    await message.answer(format_result(data), reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

async def main():
    await dp.start_polling(bot)

def get_option_key(question_id: str, user_text: str) -> str | None:
    options = QUESTIONS[question_id]["options"]
    for key, text in options.items():
        if text == user_text:
            return key
    return None


if __name__ == "__main__":
    asyncio.run(main())
