from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def night_keyboard(players):
    keyboard = []

    for player in players:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=player["name"],
                    callback_data=f"night_{player['id']}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
