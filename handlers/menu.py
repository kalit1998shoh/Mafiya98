
from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "🎮 Public o'yin")
async def public_game(message: Message):
    await message.answer(
        "🎮 Public o'yin bo'limi hozir ishlab chiqilmoqda."
    )


@router.message(F.text == "🔒 Private Club")
async def private_club(message: Message):
    await message.answer(
        "🔒 Private Club bo'limi hozir ishlab chiqilmoqda."
    )


@router.message(F.text == "👤 Profil")
async def profile(message: Message):
    await message.answer(
        "👤 Profil bo'limi."
    )


@router.message(F.text == "🏆 Reyting")
async def rating(message: Message):
    await message.answer(
        "🏆 Reyting bo'limi."
    )


@router.message(F.text == "📖 Qoidalar")
async def rules(message: Message):
    await message.answer(
        "📖 O'yin qoidalari."
    )


@router.message(F.text == "⚙️ Sozlamalar")
async def settings(message: Message):
    await message.answer(
        "⚙️ Sozlamalar bo'limi."
    )
