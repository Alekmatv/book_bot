from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def bookmarks_kb(bookmarks: set) -> InlineKeyboardMarkup:
    '''Функция возвращает клавиатуру с закладками пользователя'''

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buttons: InlineKeyboardButton = [InlineKeyboardButton(
        text=f'{bm[0]} стр. {bm[1].lstrip()}...',
        callback_data=bm[0])
        for bm in sorted(bookmarks)]
    special_buttons = [InlineKeyboardButton(text='Редактировать ⚙️',
                                            callback_data='edit_bm'),
                       InlineKeyboardButton(text='Назад',
                                            callback_data='come_back')]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(*special_buttons)

    return kb_builder.as_markup()


def edit_bookmarks_kb(bookmarks: set) -> InlineKeyboardMarkup:
    '''Функция возвращает клавиатуру с закладками пользователя'''

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buttons: InlineKeyboardButton = [InlineKeyboardButton(
        text=f'❌ {bm[0]} стр. {bm[1].lstrip()}...',
        callback_data=f'del{bm[0]}')
        for bm in sorted(bookmarks)]
    special_buttons = [InlineKeyboardButton(text='Назад',
                                            callback_data='cancel_del')]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(*special_buttons)

    return kb_builder.as_markup()


def deletion_confirmation(bookmark):
    '''Функция возвращает клавиатуру да/нет'''

    yes_butt: InlineKeyboardButton = InlineKeyboardButton(
        text='Да',
        callback_data=f'yes{bookmark}')

    no_butt: InlineKeyboardButton = InlineKeyboardButton(
        text='Нет',
        callback_data='no')

    return InlineKeyboardMarkup(inline_keyboard=[[yes_butt, no_butt]])
