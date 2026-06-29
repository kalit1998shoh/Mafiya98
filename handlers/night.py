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
                
@router.callback_query(F.data.startswith("night_"))
async def night_callback(callback: CallbackQuery):
    player_id = callback.from_user.id

    if player_id not in game.players:
        return

    if not game.players[player_id]["alive"]:
        return

    target = int(callback.data.split("_")[1])

    role = game.players[player_id]["role"]

    if role == "🔫 Mafiya":
        game.mafia_target = target
        await callback.answer("Qurbon tanlandi.")

    elif role == "💉 Doktor":
        game.doctor_save = target
        await callback.answer("Bemor saqlandi.")

    elif role == "👮 Komissar":
        game.commissioner_check = target

        tekshirildi = game.players[target]["role"]

        if tekshirildi == "🔫 Mafiya":
            text = "✅ Bu o'yinchi MAFIYA."
        else:
            text = "❌ Bu o'yinchi mafiya emas."

        await callback.message.answer(text)
        await callback.answer()

    # Uchala rol ham harakat qilgan bo'lsa tongga o'tamiz
    if (
        game.mafia_target is not None
        and game.doctor_save is not None
        and game.commissioner_check is not None
    ):
        await finish_night(callback.bot)

async def finish_night(bot):
    # Qurbonni aniqlash
    if game.mafia_target == game.doctor_save:
        natija = "💉 Doktor qurbonni qutqarishga muvaffaq bo'ldi."
    else:
        if game.mafia_target is not None:
            game.players[game.mafia_target]["alive"] = False
            natija = (
                f"☠️ {game.players[game.mafia_target]['name']} o'ldirildi."
            )
        else:
            natija = "🌙 Bu tun hech kim o'lmadi."

    # Keyingi tun uchun tozalash
    game.mafia_target = None
    game.doctor_save = None
    game.commissioner_check = None

    game.phase = "discussion"

    # Tong xabari
    for player_id, data in game.players.items():
        if data["alive"]:
            try:
                await bot.send_message(
                    player_id,
                    "🌅 Tong otdi!\n\n"
                    f"{natija}\n\n"
                    "🗣 Muhokama uchun 60 soniya."
                )
            except:
                pass

    # 60 soniya kutish
    await asyncio.sleep(60)

    # Ovoz berish bosqichi
    game.phase = "voting"

    for player_id, data in game.players.items():
        if data["alive"]:
            try:
                await bot.send_message(
                    player_id,
                    "🗳 Muhokama tugadi.\n\n"
                    "Endi ovoz berish boshlanadi."
                )
            except:
                pass



