import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

from api import APIClient

load_dotenv()

api_client = APIClient(getenv("SERVER_URL"))

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def get_studymodes(message: Message):
    study_modes = api_client.get_study_modes()

    buttons = [InlineKeyboardButton(text=mode.name, callback_data=f"studymode_{mode.id}") for mode in study_modes]

    buttons.append(InlineKeyboardButton(text="Я первокурсник", callback_data="freshman"))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.answer(
        f"Приветствую, {html.bold(message.from_user.full_name)}!\n"
        "Я - бот Ботан от ГрадМастер!\n\n"
        "Здесь ты можешь заказать работы и узнать важную информацию о сессии.\n\n"
        "Чтобы заказать работы - выбери свою форму обучения.\n"
        "Чтобы узнать информацию по сессии для 1 курса - нажми «Я - первокурсник!»",
        reply_markup=keyboard)


@dp.callback_query(lambda callback_query: callback_query.data.startswith("studymode_"))
async def get_courses(callback_query: CallbackQuery):
    study_mode_id = int(callback_query.data.split("_")[1])
    selected_study_mode = api_client.get_study_mode_by_id(study_mode_id)
    print(selected_study_mode)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=course.name, callback_data=f"course_{course.id}") for course in
         selected_study_mode.courses]
    ])
    await callback_query.message.answer(
        f"Вы выбрали {html.bold(selected_study_mode.name)}. Укажите курс обучения:",
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback_query: callback_query.data.startswith("course_"))
async def get_semesters(callback_query: CallbackQuery):
    course_id = int(callback_query.data.split("_")[1])
    selected_course = api_client.get_course_by_id(course_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=semester.name, callback_data=f"semester_{semester.id}") for semester in
         selected_course.semesters]])

    await callback_query.message.answer(
        f"Вы выбрали курс {html.bold(selected_course.name)}. Укажите семестр:",
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback_query: callback_query.data.startswith("semester_"))
async def get_groups(callback_query: CallbackQuery):
    semester_id = int(callback_query.data.split("_")[1])
    selected_semester = api_client.get_semester_by_id(semester_id)

    # Создаем кнопки для всех групп
    buttons = [InlineKeyboardButton(text=group.name,
                                    web_app=WebAppInfo(
                                        url=f"{getenv('MINIAPP_URL')}/miniapp/{group.id}")
                                    ) for group in selected_semester.groups]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[i:i + 7] for i in range(0, len(buttons), 7)]
    )

    await callback_query.message.answer(
        f"Вы выбрали семестр {html.bold(selected_semester.name)}. Выберите специальность:",
        reply_markup=keyboard
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
