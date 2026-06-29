from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def night_keyboard(players):
    keyboard = []

    for player_id, data in players.items():
        if data["alive"]:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=data["name"],
                        callback_data=f"night_{player_id}"
                    )
                ]
            )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
