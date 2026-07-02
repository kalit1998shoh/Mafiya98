from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import game
from handlers.night import start_night

router = Router()


async def start_vote(bot):
    game.phase = "vote"
    game.votes.clear()

    keyboard = []

    for player_id, data in game.players.items():
        if not data["alive"]:
            continue

        keyboard.append([
            InlineKeyboardButton(
                text=data["name"],
                callback_data=f"vote:{player_id}"
            )
        ])

    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

    for player_id, data in game.players.items():
        if not data["alive"]:
            continue

        await bot.send_message(
            player_id,
            "🗳 Kimni ovozdan chiqarishni tanlang.",
            reply_markup=markup
        )
        
@router.callback_query(F.data.startswith("vote:"))
async def vote_callback(callback: CallbackQuery):
    voter = callback.from_user.id

    if voter not in game.players:
        return

    if not game.players[voter]["alive"]:
        await callback.answer(
            "❌ Siz tirik emassiz!",
            show_alert=True
        )
        return

    if voter in game.votes:
        await callback.answer(
            "❌ Siz allaqachon ovoz bergansiz!",
            show_alert=True
        )
        return

    target = int(callback.data.split(":")[1])

    if target not in game.players:
        await callback.answer(
            "❌ O'yinchi topilmadi!",
            show_alert=True
        )
        return

    if not game.players[target]["alive"]:
        await callback.answer(
            "❌ Bu o'yinchi allaqachon o'lgan!",
            show_alert=True
        )
        return

    game.votes[voter] = target

    await callback.answer("✅ Ovoz qabul qilindi!")

    alive_count = sum(
        1 for data in game.players.values()
        if data["alive"]
    )

    if len(game.votes) >= alive_count:
        await count_votes(callback.bot)
       
async def count_votes(bot):
    results = {}

    for target in game.votes.values():
        results[target] = results.get(target, 0) + 1

    if not results:
        await start_night(bot)
        return

    max_votes = max(results.values())

    eliminated = [
        player_id
        for player_id, count in results.items()
        if count == max_votes
    ]

    # Durang
    if len(eliminated) > 1:
        for player_id, data in game.players.items():
            if data["alive"]:
                await bot.send_message(
                    player_id,
                    "⚖️ Ovozlar teng bo'ldi. Hech kim chiqarilmadi."
                )

        await start_night(bot)
        return

    target = eliminated[0]

    game.players[target]["alive"] = False
    game.alive_players.discard(target)
    game.dead_players.add(target)

    role = game.players[target]["role"]
    name = game.players[target]["name"]

    for player_id, data in game.players.items():
        if data["alive"]:
            await bot.send_message(
                game.group_id,
                f"☠️ {name} ovoz berish orqali chiqarildi.\n"
                f"Uning roli: {role}"
            )

    winner = game.check_winner()

    if winner:
        await finish_game(bot, winner)
    else:
        await start_night(bot)

async def finish_game(bot, winner):
    if winner == "🔫 Mafia":
        text = (
            "🏴 O'yin tugadi!\n\n"
            "🔫 Mafiya g'alaba qozondi!"
        )
    else:
        text = (
            "🏡 O'yin tugadi!\n\n"
            "👥 Aholi g'alaba qozondi!"
        )

    # Rollarni ko'rsatish
    roles_text = "\n\n🎭 Rollar:\n"

    for player_id, data in game.players.items():
        roles_text += (
            f"{data['name']} — {data['role']}\n"
        )

    text += roles_text

    for player_id in game.players.keys():
        try:
            await bot.send_message(player_id, text)
        except Exception:
            pass

    game.reset_game()
