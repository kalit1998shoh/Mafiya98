from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.photo)
async def get_photo_id(message: Message):
    photo = message.photo[-1]

    await message.answer(
        f"📷 file_id:\n\n<code>{photo.file_id}</code>",
        parse_mode="HTML"
    )
