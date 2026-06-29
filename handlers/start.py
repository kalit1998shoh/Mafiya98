from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎮 Mafiya98 ga xush kelibsiz!\n\n"
        "🚧 Bot hozir ishlab chiqilmoqda."
    )
