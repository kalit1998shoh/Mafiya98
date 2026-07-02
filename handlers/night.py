import asyncio

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import game
from keyboards.night import night_keyboard

router = Router()


async def start_night(bot):
    game.phase = "night"

    # Banner
    await bot.send_photo(
        chat_id=game.group_id,
        photo="AgACAgIAAxkBAAIEJ2pFgrR28dRZnVkg6poMagWBDL7uAAIQHmsbpS8pShd7gfwprSMvAQADAgADeQADPAQ",
        caption=(
            "🌙 <b>TUN</b>\n\n"
            "Ko'chaga faqat jasur va qo'rqmas odamlar chiqishdi...\n\n"
            "🌃 Shahar uyquga ketdi.\n"
            "🤫 Ertalab tirik qolganlarni sanaymiz..."
        ),
        parse_mode="HTML"
    )

    await asyncio.sleep(2)

    # Tozalash
    game.mafia_target = None
    game.doctor_save = None
    game.commissioner_check = None
    game.maniac_target = None

    # Tirik o'yinchilarga xabar
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

    # Mafiya
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

    # Doktor
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

    # Komissar
    for player_id, data in game.players.items():
        if data["alive"] and data["role"] == "👮 Komissar":
            try:
                if game.day == 1 or game.commissioner_used_shot:

                    game.commissioner_action = "check"

                    await bot.send_message(
                        player_id,
                        "👮 Kimni tekshirasiz?",
                        reply_markup=night_keyboard(game.players)
                    )

                else:

                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="🔍 Tekshirish",
                                    callback_data="comm_check"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="🔫 Otish",
                                    callback_data="comm_shoot"
                                )
                            ]
                        ]
                    )

                    await bot.send_message(
                        player_id,
                        "👮 Amalni tanlang.",
                        reply_markup=keyboard
                    )

            except Exception as e:
                print(f"Komissar xatosi: {e}")

    # Manyak
    for player_id, data in game.players.items():
        if data["alive"] and data["role"] == "🔪 Manyak":
            try:
                await bot.send_message(
                    player_id,
                    "🔪 Kimni o'ldirasiz?",
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

        if game.commissioner_action == "check":
            tekshirildi = game.players[target]["role"]

            if tekshirildi == "🔫 Mafiya":
                await callback.message.answer("✅ Bu o'yinchi MAFIYA.")
            else:
                await callback.message.answer("❌ Bu o'yinchi mafiya emas.")

        await callback.answer()

    elif role == "🔪 Manyak":
        game.maniac_target = target
        await callback.answer("Qurbon tanlandi.")

    # Agar hamma harakat qilgan bo'lsa tunni tugatish
    if (
        game.mafia_target is not None
        and game.doctor_save is not None
        and game.commissioner_check is not None
        and game.maniac_target is not None
    ):
        await finish_night(callback.bot)


async def finish_night(bot):

    # Mafiya natijasi
    if game.mafia_target == game.doctor_save:
        natija = "💉 Doktor qurbonni qutqarishga muvaffaq bo'ldi."
    else:
        if game.mafia_target is not None:
            game.players[game.mafia_target]["alive"] = False
            game.alive_players.discard(game.mafia_target)
            game.dead_players.add(game.mafia_target)

            natija = (
                f"☠️ {game.players[game.mafia_target]['name']} o'ldirildi."
            )
        else:
            natija = "🌙 Bu tun hech kim o'lmadi."

    # Manyak
    if (
        game.maniac_target is not None
        and game.maniac_target != game.doctor_save
    ):
        game.players[game.maniac_target]["alive"] = False
        game.alive_players.discard(game.maniac_target)
        game.dead_players.add(game.maniac_target)

    # Tozalash
    game.mafia_target = None
    game.doctor_save = None
    game.commissioner_check = None
    game.maniac_target = None

    game.phase = "discussion"

    # Tong
    await bot.send_message(
        game.group_id,
        "🌅 Tong otdi!\n\n"
        f"{natija}\n\n"
        "🗣 Muhokama uchun 60 soniya."
    )

    await asyncio.sleep(60)

    game.phase = "voting"

    await bot.send_message(
        game.group_id,
        "🗳 Muhokama tugadi!\n\n"
        "📩 Bot sizga shaxsiy chatda ovoz berish tugmalarini yubordi."
    )

    from handlers.vote import start_vote
    await start_vote(bot)
