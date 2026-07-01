from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import game
from roles import give_roles
from handlers.night import start_night

router = Router()


# ==========================
# PUBLIC LOBBY
# ==========================

@router.message(Command("play"))
async def public_game(message: Message):

    if game.game_started:
        await message.answer(
            "❌ O'yin allaqachon boshlangan."
        )
        return

    # Yangi lobby
    game.group_id = message.chat.id
    game.lobby_owner = message.from_user.id

    # Eski o'yinchilarni tozalash
    game.players.clear()
    game.roles.clear()
    game.alive_players.clear()

    # Lobby egasini qo'shamiz
    game.players[message.from_user.id] = {
        "id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username,
        "role": None,
        "alive": True,
    }

    count = len(game.players)

    await message.answer(
        f"🎮 Public Lobby\n\n"
        f"👥 O'yinchilar: {count}\n\n"
        f"📩 Boshqalar /join orqali qo'shilishi mumkin.\n"
        f"▶️ 4 ta o'yinchi yig'ilgach /startgame yozing."
    )


# ==========================
# JOIN
# ==========================

@router.message(Command("join"))
async def join_game(message: Message):

    # Botga start bosmagan
    if message.from_user.id not in game.started_users:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🤖 Botga Start berish",
                        url="https://t.me/Mafiya1998_bot?start=join"
                    )
                ]
            ]
        )

        await message.answer(
            "❌ Siz hali botga Start bermagansiz.\n\n"
            "👇 Avval botga kirib Start bosing, keyin yana /join yozing.",
            reply_markup=keyboard
        )
        return

    # Lobby mavjud emas
    if game.lobby_owner is None:
        await message.answer(
            "❌ Avval /play orqali lobby ochilishi kerak."
        )
        return

    # O'yin boshlangan
    if game.game_started:
        await message.answer(
            "❌ O'yin allaqachon boshlangan."
        )
        return

    # Allaqachon o'yinda
    if message.from_user.id in game.players:
        await message.answer(
            "❌ Siz allaqachon o'yindasiz."
        )
        return

    # O'yinchini qo'shamiz
    game.players[message.from_user.id] = {
        "id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username,
        "role": None,
        "alive": True,
    }

    count = len(game.players)

    await message.answer(
        f"✅ {message.from_user.full_name} o'yinga qo'shildi.\n\n"
        f"👥 O'yinchilar: {count}"
    )


# ==========================
# START GAME
# ==========================

@router.message(Command("startgame"))
async def start_game(message: Message):

    # Faqat lobby egasi
    if message.from_user.id != game.lobby_owner:
        await message.answer(
            "❌ Faqat lobby yaratgan o'yinchi o'yinni boshlashi mumkin."
        )
        return

    # Kamida 4 o'yinchi
    if len(game.players) < 4:
        await message.answer(
            "❌ O'yinni boshlash uchun kamida 4 ta o'yinchi kerak."
        )
        return

    ids = list(game.players.keys())

    # Rollarni taqsimlash
    game.roles = give_roles(ids)

    game.alive_players.clear()

    for player_id, role in game.roles.items():

        game.players[player_id]["role"] = role
        game.players[player_id]["alive"] = True

        game.alive_players.add(player_id)

    # Rollarni shaxsiy chatga yuboramiz
    for player_id, role in game.roles.items():

        try:
            await message.bot.send_message(
                chat_id=player_id,
                text=(
                    "🎭 Sizning rolingiz\n\n"
                    f"🔹 {role}\n\n"
                    "❗ Rolingizni hech kimga aytmang."
                )
            )

        except Exception:
            await message.answer(
                f"❌ {game.players[player_id]['name']} botga Start bermagan.\n\n"
                "O'yin boshlanmadi."
            )
            return

    # O'yin boshlandi
    game.game_started = True

    await message.bot.send_message(
        chat_id=game.group_id,
        text=(
            "🎮 O'yin boshlandi!\n\n"
            "📨 Rollar barcha o'yinchilarga shaxsiy chat orqali yuborildi.\n"
            "🌙 Tun boshlandi..."
        )
    )

    # Tungi bosqichni boshlash
    await start_night(message.bot)
