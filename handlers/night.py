from aiogram import Router

import game

router = Router()


async def start_night(bot):
    game.phase = "night"

    for player_id in game.alive_players:
        role = game.roles.get(player_id)

        if role == "🔫 Mafiya":
            await bot.send_message(
                player_id,
                "🌙 Tun boshlandi.\n\n🔫 Qurbonni tanlang."
            )

        elif role == "💉 Doktor":
            await bot.send_message(
                player_id,
                "🌙 Tun boshlandi.\n\n💉 Kimni davolaysiz?"
            )

        elif role == "👮 Komissar":
            await bot.send_message(
                player_id,
                "🌙 Tun boshlandi.\n\n👮 Kimni tekshirasiz?"
            )

        else:
            await bot.send_message(
                player_id,
                "🌙 Tun. Harakat qilish uchun kuting."
            )
