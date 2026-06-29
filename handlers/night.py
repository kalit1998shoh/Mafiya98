from aiogram import Router, F
from aiogram.types import CallbackQuery
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

# Tun natijasi
if game.mafia_target is not None:

    if game.mafia_target != game.doctor_save:

        game.players[game.mafia_target]["alive"] = False
        game.dead_players.add(game.mafia_target)

        natija = (
            f"☠️ Kechasi {game.players[game.mafia_target]['name']} o'ldirildi."
        )

    else:
        natija = "💉 Doktor qurbonni qutqarishga muvaffaq bo'ldi."

else:
    natija = "🌙 Bu tun hech kim o'lmadi."

# Keyingi tun uchun tozalash
game.mafia_target = None
game.doctor_save = None
game.commissioner_check = None

game.phase = "discussion"

for player_id, data in game.players.items():
    if data["alive"]:
        try:
            await bot.send_message(
                player_id,
                f"🌅 Tong otdi!\n\n"
                f"{natija}\n\n"
                "🗣 Muhokama uchun 60 soniya."
            )
        except:
            pass


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

            
