from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def night_keyboard(players):
    keyboard = []

    for player_id in players:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"👤 {player_id}",
                    callback_data=f"night_{player_id}"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
