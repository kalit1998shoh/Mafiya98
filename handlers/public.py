from roles import give_roles

import random

from aiogram import Router, F, Bot
from aiogram.types import Message

from keyboards.public import public_menu
import game

router = Router()


@router.message(F.text == "🎮 Public o'yin")
async def public_game(message: Message):

    if game.game_started:
        await message.answer("🚫 O'yin allaqachon boshlangan.")
        return

    if message.from_user.id in game.players:
        await message.answer(
            f"✅ Siz allaqachon Lobbydasiz.\n\n"
            f"👥 O'yinchilar: {len(game.players)}"
        )
        return

    game.players.add(message.from_user.id)

    if len(game.players) >= 4:
        await message.answer(
            f"🎮 Public Lobby\n\n"
            f"👥 O'yinchilar: {len(game.players)}\n\n"
            f"▶️ Endi o'yinni boshlash mumkin.",
            reply_markup=public_menu
        )
    else:
        await message.answer(
            f"🎮 Public Lobby\n\n"
            f"👥 O'yinchilar: {len(game.players)}\n\n"
            f"⏳ Kamida 4 ta o'yinchi kerak."
        )
