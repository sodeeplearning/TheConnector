from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from backend.keyboards import categories_buttons, short_video_buttons, long_video_buttons
from backend.utils.get_video import get_video_from_category
from backend.utils.agent import AIAgent, AIAgentRequestModel

import config


router = Router()

ai_agent = AIAgent()


class WatchVideo(StatesGroup):
    choosing_category = State()
    short_video_waiting = State()
    long_video_waiting = State()
    ask_ai = State()


@router.message(Command("watch"))
async def watch_video(message: types.Message, state: FSMContext):
    await state.set_state(WatchVideo.choosing_category)
    await message.answer("Выберете категорию:", reply_markup=categories_buttons)


@router.callback_query(F.data == "watch")
async def callback_watch_video(callback: types.CallbackQuery, state: FSMContext):
    await watch_video(message=callback.message, state=state)


@router.callback_query(F.data.in_(config.categories), WatchVideo.choosing_category)
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data
    await state.update_data(category=category)
    await callback.answer()
    await send_short_video(callback=callback, state=state)


@router.callback_query(F.data == "next_video")
async def send_short_video(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(WatchVideo.short_video_waiting)
    data = await state.get_data()
    short_video = get_video_from_category(data["category"])
    await state.update_data(last_video=short_video)

    await callback.message.answer_video(
        types.FSInputFile(short_video.short_video_path),
        reply_markup=short_video_buttons
    )


@router.callback_query(F.data == "full_video")
async def send_long_video(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(WatchVideo.long_video_waiting)
    data = await state.get_data()
    short_video = data["last_video"]
    long_video = types.FSInputFile(short_video.full_video_path)
    await callback.message.answer_video(long_video, reply_markup=long_video_buttons)


@router.message(F.data == "ask_ai")
async def ask_ai(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(WatchVideo.ask_ai)
    await callback.message.answer("Введите запрос к ИИ агенту")


@router.message(F.text, WatchVideo.ask_ai)
async def give_ai_response(message: types.Message, state: FSMContext):
    response = await ai_agent(AIAgentRequestModel(text=message.text))
    await message.answer(response.text)

