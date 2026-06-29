from aiogram import Router, F
from aiogram.types import Message

from keyboards.public import public_menu

router = Router()

players = set()


@router.message(F.text == "🎮 Public o'yin")
async def public_game(message: Message):

    if message.from_user.id in players:
        await message.answer(
            f"✅ Siz allaqachon Lobbydasiz.\n\n"
            f"👥 O'yinchilar soni: {len(players)}"
        )
        return

    players.add(message.from_user.id)

    if len(players) >= 4:
        await message.answer(
            f"🎮 Public Lobby\n\n"
            f"👥 O'yinchilar soni: {len(players)}\n\n"
            f"✅ Endi o'yinni boshlash mumkin.",
            reply_markup=public_menu
        )
    else:
        await message.answer(
            f"🎮 Public Lobby\n\n"
            f"👥 O'yinchilar soni: {len(players)}\n\n"
            f"⏳ Kamida 4 ta o'yinchi kerak."
        )
