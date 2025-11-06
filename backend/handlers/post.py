from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import config
from backend.utils.post_video import save_and_split_video


router = Router()


class UploadVideo(StatesGroup):
    choosing_category = State()
    waiting_video = State()


@router.message(Command("post"), F.data.is_("post"))
async def post_video(message: types.Message, state: FSMContext):
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c, callback_data=c)]
            for c in config.categories
        ]
    )
    await state.set_state(UploadVideo.choosing_category)
    await message.reply("Выберете категорию видео: ", reply_markup=buttons)



@router.callback_query(F.data.in_(config.categories))
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data
    await state.update_data(category=category)
    await state.set_state(UploadVideo.waiting_video)
    await callback.message.answer(f"Категория выбрана: {category}\nТеперь загрузите видео")
    await callback.answer()


@router.message(F.video, UploadVideo.waiting_video)
async def process_video(message: types.Message, state: FSMContext):
    data = await state.get_data()
    video_category = data["category"]

    bot = message.bot
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    video_bytes = await bot.download_file(file.file_path)
    video_bytes = video_bytes.read()

    save_and_split_video(
        video_bytes=video_bytes,
        file_name=file.file_id,
        video_category=video_category,
    )

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выложить еще одно видео", callback_data="post")],
        [InlineKeyboardButton(text="Приступить к просмотру", callback_data="watch")],
    ])

    await message.reply("Вы выложили видео! Что теперь желаете?", reply_markup=buttons)
