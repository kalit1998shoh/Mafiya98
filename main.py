import asyncio
import logging
from handlers.night import router as night_router

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.public import router as public_router
from handlers.vote import router as vote_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Routerlarni ulash
dp.include_router(start_router)
dp.include_router(menu_router)
dp.include_router(public_router)
dp.include_router(night_router)
dp.include_router(vote_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
