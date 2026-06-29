from roles import give_roles

import random

from aiogram import Router, F, Bot
from aiogram.types import Message

from keyboards.public import public_menu
import game

router = Router()


@router.message(F.text == "🎮 Public o'yin")
async def public_game(message: Message):

    game.players.add(message.from_user.id)

    await message.answer(
        f"👥 O'yinchilar: {len(game.players)}"
    )

    if len(game.players) >= 4 and not game.game_started:
        game.game_started = True
        game.roles = give_roles(game.players)

        for player_id, role in game.roles.items():
            try:
                await message.bot.send_message(
                    player_id,
                    f"🎭 Sizning rolingiz:\n\n{role}"
                )
            except:
                pass

        await message.answer(
            "🎉 4 ta o'yinchi yig'ildi!\n"
            "🎭 Rollar tarqatildi.\n"
            "🌙 O'yin boshlandi!"
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
