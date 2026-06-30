from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message
from handlers.night import start_night

import game
from roles import give_roles
from keyboards.public import public_menu

router = Router()


@router.message(Command("play"))
async def public_game(message: Message):

    # O'yin boshlangan bo'lsa yangi o'yinchi qo'shilmaydi
    
    game.group_id = message.chat.id
    game.lobby_owner = message.from_user.id
    
    if game.game_started:
        await message.answer(
            "❌ O'yin allaqachon boshlangan."
        )
        return

    # O'yinchi oldin qo'shilmagan bo'lsa qo'shamiz
    if message.from_user.id not in game.players:

        game.players[message.from_user.id] = {
            "id": message.from_user.id,
            "name": message.from_user.full_name,
            "username": message.from_user.username,
            "role": None,
            "alive": True
        }

    player_count = len(game.players)

    # 4 ta bo'lmasa kutadi
    if player_count < 4:
        await message.answer(
            f"🎮 Public Lobby\n\n"
            f"👥 O'yinchilar: {player_count}\n\n"
            f"⏳ Kamida 4 ta o'yinchi kerak."
        )
        return

    # O'yinni boshlash
    game.game_started = True

    ids = list(game.players.keys())

    game.roles = give_roles(ids)

    for player_id, role in game.roles.items():

        game.players[player_id]["role"] = role
        game.alive_players.add(player_id)

        try:
            await message.bot.send_message(
                player_id,
                f"🎭 Sizning rolingiz:\n\n{role}"
            )
        except:
            pass

    await message.answer(
        "🎉 4 ta o'yinchi yig'ildi!\n\n"
        "🎭 Rollar tarqatildi.\n"
        "🌙 O'yin boshlandi!",
        reply_markup=public_menu
    )

    await start_night(message.bot)
@router.message(Command("join"))
async def join_game(message: Message):

    if not game.game_started:
        await message.answer(
            "❌ Avval /play orqali lobby ochilishi kerak."
        )
        return

    if message.from_user.id in game.players:
        await message.answer(
            "❌ Siz allaqachon o'yindasiz."
        )
        return

    game.players[message.from_user.id] = {
        "id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username,
        "role": None,
        "alive": True
    }

    count = len(game.players)

    await message.answer(
        f"✅ {message.from_user.full_name} o'yinga qo'shildi.\n\n"
        f"👥 O'yinchilar: {count}"
    )
@router.message(Command("startgame"))
async def start_game(message: Message):

    if len(game.players) < 4:
        await message.answer(
            "❌ O'yinni boshlash uchun kamida 4 ta o'yinchi kerak."
        )
        return

    ids = list(game.players.keys())

    game.roles = give_roles(ids)

    game.alive_players.clear()

    for player_id, role in game.roles.items():

        game.players[player_id]["role"] = role
        game.players[player_id]["alive"] = True

        game.alive_players.add(player_id)

        try:
            await message.bot.send_message(
                player_id,
                f"🎭 Sizning rolingiz:\n\n{role}"
            )
        except:
            pass

    await message.answer(
        "🎉 O'yin boshlandi!\n\n"
        "🌙 Rollar tarqatildi.\n"
        "Har bir o'yinchi bot bilan shaxsiy chatini tekshirsin."
    )

    await start_night(message.bot)


