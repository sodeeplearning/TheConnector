from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import yt_dlp

import config

from backend.utils.post_video import save_and_split_video
from backend.utils.yt_download import download_youtube_video
from backend.keyboards import categories_buttons, final_post_buttons


router = Router()


class UploadVideo(StatesGroup):
    choosing_category = State()
    waiting_video = State()



@router.message(Command("post"))
async def post_video(message: types.Message, state: FSMContext):
    await state.set_state(UploadVideo.choosing_category)
    await message.answer("Выберете категорию видео: ", reply_markup=categories_buttons)



@router.callback_query(F.data.in_(config.categories), UploadVideo.choosing_category)
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

    await state.clear()
    await message.reply("Вы выложили видео! Что теперь желаете?", reply_markup=final_post_buttons)


@router.message(F.text, UploadVideo.waiting_video)
async def process_video_link(message: types.Message, state: FSMContext):
    data = await state.get_data()
    video_category = data["category"]

    try:
        title, video_bytes = download_youtube_video(message.text)

        save_and_split_video(
            video_bytes=video_bytes,
            file_name=title + ".mp4",
            video_category=video_category,
        )

        text = "Вы выложили видео! Что теперь желаете?"
    except yt_dlp.utils.DownloadError:
        text = "Не удалось выложить видео. Проверьте корректность ссылки"
    except Exception as e:
        text = f"Неизвестная ошибка при скачивании видео: {e}"

    await state.clear()
    await message.reply(text, reply_markup=final_post_buttons)


@router.callback_query(F.data == "post")
async def callback_post_video(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await post_video(message=callback.message, state=state)
