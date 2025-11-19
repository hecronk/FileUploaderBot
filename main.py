import asyncio
from aiogram import Bot, Dispatcher, Router

from config import TELEGRAM_TOKEN
from handlers.file_handler import router as file_router
from handlers.login import router as login_router

root_router = Router()


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(root_router)
    dp.include_router(login_router)
    dp.include_router(file_router)

    print("Bot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
