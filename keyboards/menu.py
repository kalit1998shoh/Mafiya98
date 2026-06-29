from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎮 Public o'yin"),
            KeyboardButton(text="🔒 Private Club"),
        ],
        [
            KeyboardButton(text="👤 Profil"),
            KeyboardButton(text="🏆 Reyting"),
        ],
        [
            KeyboardButton(text="📖 Qoidalar"),
            KeyboardButton(text="⚙️ Sozlamalar"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Bo'limni tanlang..."
)
