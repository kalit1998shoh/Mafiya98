from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from keyboards.menu import main_menu

import game

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    
    game.started_users.add(message.from_user.id)

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
        "🎮 Mafiya98 ga xush kelibsiz!\n\n"
        "🎭 Rollar va maxfiy vazifalar shu bot orqali yuboriladi.\n"
        "💬 Muhokama va ovoz berish esa guruhda bo'ladi.\n\n"
        "👇 Avval guruhga o'ting.",
        reply_markup=keyboard
    )

    await message.answer(
        "Kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )
