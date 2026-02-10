# keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_main = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("German", callback_data="ger")],
        [InlineKeyboardButton("International", callback_data="int")],
    ]
)
keyboard_after = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Spell again", callback_data="again")],
        [InlineKeyboardButton("End", callback_data="end")],
    ]
)
