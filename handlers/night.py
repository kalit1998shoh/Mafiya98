from aiogram import Router
import asyncio
import game

router = Router()


async def start_night(bot):
    game.phase = "night"

    # Barcha o'yinchilarga tun boshlanganini yuborish
    for player_id in game.players.keys():
        try:
            await bot.send_message(
                player_id,
                "🌙 Tun boshlandi.\n\n"
                "Rolingizga qarab harakat qiling."
            )
        except:
            pass

    # Mafiyaga xabar
    for player_id, data in game.players.items():
        if data["role"] == "🔫 Mafiya":
            await bot.send_message(
                player_id,
                "🔫 Qurbonni tanlang."
            )

    # Doktorga xabar
    for player_id, data in game.players.items():
        if data["role"] == "💉 Doktor":
            await bot.send_message(
                player_id,
                "💉 Kimni qutqarasiz?"
            )

    # Komissarga xabar
    for player_id, data in game.players.items():
        if data["role"] == "👮 Komissar":
            await bot.send_message(
                player_id,
                "👮 Kimni tekshirasiz?"
            )

    # 30 soniya kutish
    await asyncio.sleep(30)

    game.phase = "discussion"

    for player_id in game.players.keys():
        try:
            await bot.send_message(
                player_id,
                "🌅 Tong otdi.\n\n"
                "🗣 Muhokama uchun 60 soniya."
            )
        except:
            pass
