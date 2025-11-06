from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from backend.keyboards import categories_buttons, short_video_buttons
from backend.utils.get_video import get_video_from_category

import config


router = Router()


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
    await state.set_state(WatchVideo.short_video_waiting)
    await callback.answer()
    await send_short_video(callback=callback, state=state)


@router.callback_query(F.data == "next_video")
async def send_short_video(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    short_video = types.FSInputFile(get_video_from_category(data["category"]).short_video_path)
    await state.update_data(last_video=short_video)
    await callback.message.answer_video(short_video, reply_markup=short_video_buttons)
