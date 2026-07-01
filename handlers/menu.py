from handlers.public import public_game
from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

router = Router()


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
    
@router.message(F.text == "🎮 Public o'yin")
async def open_public(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 O'yin guruhiga o'tish",
                    url="https://t.me/+GPftnv8c3780YjYy"
                )
            ]
        ]
    )

    await message.answer(
        "🎮 Public o'yin faqat rasmiy guruhda o'tkaziladi.\n\n"
        "👇 Pastdagi tugma orqali guruhga o'ting va u yerda /play yozing.",
        reply_markup=keyboard
    )
