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

    count = len(game.players)

    await message.answer(
        f"🎮 Public Lobby\n\n"
        f"👥 O'yinchilar: {count}\n\n"
        f"📩 Qolganlar /join orqali qo'shilishi mumkin.\n"
        f"▶️ Lobby egasi 4 ta o'yinchi yig'ilgach /startgame ni bosadi."
        )
@router.message(Command("join"))
async def join_game(message: Message):

    if not game.lobby_owner is None:
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

    if message.from_user.id != game.lobby_owner:
        await message.answer(
            "❌ Faqat lobby yaratgan o'yinchi o'yinni boshlashi mumkin."
        )
        return

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
            await message.answer(
                f"❌ {game.players[player_id]['name']} botga Start bosmagan."
            )
            continue
    
        await message.bot.send_message(
            game.group_id,
            "🌙 O'yin boshlandi!\n\n"
            "🎭 Rollar barcha o'yinchilarga shaxsiy chat orqali yuborildi.\n\n"
            "📩 Endi bot bilan shaxsiy chatni oching."
        )

        game.game_started = True

        await start_night(message.bot)
