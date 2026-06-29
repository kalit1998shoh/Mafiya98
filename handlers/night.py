import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery

import game

from keyboards.night import night_keyboard

router = Router()


async def start_night(bot):
    game.phase = "night"

    game.mafia_target = None
    game.doctor_save = None
    game.commissioner_check = None

    # Barcha tirik o'yinchilarga tun boshlandi deb yuborish
    for player_id, data in game.players.items():
        if not data["alive"]:
            continue

        try:
            await bot.send_message(
                player_id,
                "🌙 Tun boshlandi.\n\n"
                "Rolingizga qarab harakat qiling."
            )
        except:
            pass

    # Mafiyaga tanlash
    for player_id, data in game.players.items():
        if data["alive"] and data["role"] == "🔫 Mafiya":
            try:
                await bot.send_message(
                    player_id,
                    "🔫 Qurbonni tanlang.",
                    reply_markup=night_keyboard(game.players)
                )
            except:
                pass

    # Doktorga tanlash
    for player_id, data in game.players.items():
        if data["alive"] and data["role"] == "💉 Doktor":
            try:
                await bot.send_message(
                    player_id,
                    "💉 Kimni qutqarasiz?",
                    reply_markup=night_keyboard(game.players)
                )
            except:
                pass

    # Komissarga tanlash
    for player_id, data in game.players.items():
        if data["alive"] and data["role"] == "👮 Komissar":
            try:
                await bot.send_message(
                    player_id,
                    "👮 Kimni tekshirasiz?",
                    reply_markup=night_keyboard(game.players)
                )
            except:
                pass
