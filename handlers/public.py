from aiogram import Router, F
from aiogram.types import Message

router = Router()

players = set()

@router.message(F.text == "🎮 Public o'yin")
async def public_game(message: Message):
    players.add(message.from_user.id)

    await message.answer(
        f"🎮 Public Lobby\n\n"
        f"👥 O'yinchilar soni: {len(players)}\n\n"
        f"Yana o'yinchilar qo'shilishini kuting..."
    )
