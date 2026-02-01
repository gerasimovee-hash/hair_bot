import asyncio
from content_loader import load_content, build_description
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

@dp.message(HairTest.thickness)
async def thickness_step(message: types.Message, state: FSMContext):
    key = get_option_key("thickness", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(thickness=key)

    await state.set_state(HairTest.density)
    q = QUESTIONS["density"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message(HairTest.density)
async def density_step(message: types.Message, state: FSMContext):
    key = get_option_key("density", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(density=key)

    await state.set_state(HairTest.scalp)
    q = QUESTIONS["scalp"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message(HairTest.scalp)
async def scalp_step(message: types.Message, state: FSMContext):
    key = get_option_key("scalp", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(scalp=key)

    await state.set_state(HairTest.length)
    q = QUESTIONS["length"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message(HairTest.length)
async def length_step(message: types.Message, state: FSMContext):
    key = get_option_key("length", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(length=key)

    await state.set_state(HairTest.porosity)
    q = QUESTIONS["porosity"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message(HairTest.porosity)
async def porosity_step(message: types.Message, state: FSMContext):
    key = get_option_key("porosity", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(porosity=key)

    await state.set_state(HairTest.damage)
    q = QUESTIONS["damage"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message(HairTest.damage)
async def damage_step(message: types.Message, state: FSMContext):
    key = get_option_key("damage", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(damage=key)

    await state.set_state(HairTest.age)
    q = QUESTIONS["age"]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message(HairTest.age)
async def finish(message: types.Message, state: FSMContext):
    key = get_option_key("age", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    await state.update_data(age=key)

    data = await state.get_data()
    data = apply_corrections(data)

    await message.answer(
        format_result(data),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

# ⚠️ Аналогично добавляются остальные шаги (я могу дописать полностью)

from aiogram.types import ReplyKeyboardRemove

@dp.message(HairTest.age)
async def finish(message: types.Message, state: FSMContext):
    # 1) переводим текст кнопки → код
    key = get_option_key("age", message.text)
    if not key:
        await message.answer("Пожалуйста, выбери вариант с кнопки 👇")
        return

    # 2) сохраняем код
    await state.update_data(age=key)

    # 3) собираем профиль и применяем автокоррекции
    data = await state.get_data()
    data = apply_corrections(data)

    # 4) грузим контент и строим финальное описание
    content = load_content("content.yml")
    text = build_description(data, content)

    # 5) отправляем
    await message.answer(text, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")

    # 6) очищаем состояние
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
