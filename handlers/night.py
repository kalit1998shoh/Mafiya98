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
from aiogram import F
from aiogram.types import CallbackQuery


@router.callback_query(F.data.startswith("night_"))
async def night_choice(callback: CallbackQuery):

    if game.phase != "night":
        await callback.answer("Tun tugagan.")
        return

    target_id = int(callback.data.split("_")[1])

    role = game.players[callback.from_user.id]["role"]

    if role == "🔫 Mafiya":
        game.mafia_target = target_id
        await callback.answer("Qurbon tanlandi.")
        await callback.message.edit_text("✅ Siz qurbonni tanladingiz.")

    elif role == "💉 Doktor":
        game.doctor_save = target_id
        await callback.answer("O'yinchi qutqarildi.")
        await callback.message.edit_text("✅ Siz bemorni tanladingiz.")

    elif role == "👮 Komissar":
        game.commissioner_check = target_id

        tekshiruv = game.players[target_id]["role"]

        if tekshiruv == "🔫 Mafiya":
            natija = "🔫 Mafiya"
        else:
            natija = "🙂 Mafiya emas"

        await callback.message.edit_text(
            f"🔎 Natija:\n\n{natija}"
        )

        await callback.answer()

            
