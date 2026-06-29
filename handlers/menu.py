from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda message: message.text == "🎮 Public o'yin")
async def public_game(message: Message):
    await message.answer("🎮 Public o'yin bo'limi hozir ishlab chiqilmoqda.")

@router.message(lambda message: message.text == "🔒 Private Club")
async def private_club(message: Message):
    await message.answer("🔒 Private Club bo'limi hozir ishlab chiqilmoqda.")

@router.message(lambda message: message.text == "👤 Profil")
async def profile(message: Message):
    await message.answer("👤 Profil bo'limi.")

@router.message(lambda message: message.text == "🏆 Reyting")
async def rating(message: Message):
    await message.answer("🏆 Reyting bo'limi.")

@router.message(lambda message: message.text == "📖 Qoidalar")
async def rules(message: Message):
    await message.answer("📖 O'yin qoidalari.")

@router.message(lambda message: message.text == "⚙️ Sozlamalar")
async def settings(message: Message):
    await message.answer("⚙️ Sozlamalar bo'limi.")
