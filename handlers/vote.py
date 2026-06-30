from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import game
from handlers.night import start_night

router = Router()


async def start_vote(bot):
    game.phase = "vote"
    game.votes.clear()

    keyboard = []

    for player_id in game.alive_players:
        keyboard.append([
            InlineKeyboardButton(
                text=game.players[player_id]["name"],
                callback_data=f"vote:{player_id}"
            )
        ])

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    for player_id in game.alive_players:
        await bot.send_message(
            player_id,
            "🗳 Kimni ovozdan chiqarishni tanlang:",
            reply_markup=markup
        )


@router.callback_query(F.data.startswith("vote:"))
async def vote_player(callback: CallbackQuery):
    voter = callback.from_user.id

    if voter not in game.alive_players:
        await callback.answer("Siz tirik emassiz!", show_alert=True)
        return

    if voter in game.votes:
        await callback.answer("Siz allaqachon ovoz bergansiz!", show_alert=True)
        return

    target = int(callback.data.split(":")[1])

    game.votes[voter] = target

    await callback.answer("✅ Ovoz qabul qilindi.")

    if len(game.votes) == len(game.alive_players):
        await count_votes(callback.bot)


async def count_votes(bot):
    results = {}

    for target in game.votes.values():
        results[target] = results.get(target, 0) + 1

    if not results:
        await start_night(bot)
        return

    max_votes = max(results.values())

    losers = [
        player for player, votes in results.items()
        if votes == max_votes
    ]

    if len(losers) > 1:
        for player_id in game.alive_players:
            await bot.send_message(
                player_id,
                "⚖️ Ovozlar teng bo'ldi. Hech kim chiqarilmadi."
            )

        await start_night(bot)
        return

    eliminated = losers[0]

    game.alive_players.remove(eliminated)
    game.dead_players.add(eliminated)

    role = game.roles.get(eliminated, "Noma'lum")

    for player_id in game.alive_players:
        await bot.send_message(
            player_id,
            f"☠️ {game.players[eliminated]['name']} ovoz berish orqali chiqarildi.\n"
            f"Uning roli: {role}"
        )

    winner = game.check_winner()

    if winner:
        await finish_game(bot, winner)
    else:
        await start_night(bot)


async def finish_game(bot, winner):
    if winner == "mafia":
        text = "🔴 O'yin tugadi!\n\n🏴 Mafiya g'alaba qozondi!"
    else:
        text = "🟢 O'yin tugadi!\n\n👥 Aholi g'alaba qozondi!"

    for player_id in game.players:
        await bot.send_message(player_id, text)

    game.reset_game()
