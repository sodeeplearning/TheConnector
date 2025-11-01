import asyncio

from aiogram import Bot, Dispatcher

import config
import handlers


bot = Bot(token=config.Secrets.bot_token)


async def main():
    dp = Dispatcher()
    dp.include_router(handlers.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
