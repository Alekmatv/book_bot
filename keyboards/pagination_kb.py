from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON


def _get_buttons(page: int, len_book: int) -> list:
    '''Функция проверяет является ли страница первой или последней'''
    result = ['backward', f'{page}/{len_book}', 'forward']

    if page == 1:
        result = result[1:]
    elif page == len_book:
        result = result[:2]

    return result


def create_pagination_kb(page: int, len_book: int) -> InlineKeyboardMarkup:
    '''Функция создает клавиатуру с отображением текущей страницы'''

    buttons = _get_buttons(page, len_book)

    inline_buttons = [InlineKeyboardButton(
            text=LEXICON[button] if button in LEXICON else button,
            callback_data=button) for button in buttons]

    pagination_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[inline_buttons])

    return pagination_kb
