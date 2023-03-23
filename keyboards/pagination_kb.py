from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON


def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    inline_buttons = [InlineKeyboardButton(
            text=LEXICON[button] if button in LEXICON else button,
            callback_data=button) for button in buttons]

    pagination_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[inline_buttons]
    )

    return pagination_kb
