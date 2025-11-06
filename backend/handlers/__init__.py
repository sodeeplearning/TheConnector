from aiogram import Router, types
from aiogram.filters import Command

from . import post, watch


router = Router()

router.include_routers(post.router, watch.router)


@router.message(Command("start"))
async def start_event(message: types.Message):
    await message.reply(
        text="""Приветствую вас в боте The Connector!
        
        Выберите действие:
        /post - выложить видео
        /watch - начать просмотр
        """
    )
