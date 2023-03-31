from copy import deepcopy

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from aiogram import Router

from lexicon.lexicon import LEXICON_RU, STICKERS
from database.database import (user_dict_template,
                               users_dt,
                               save_progress)
from services.file_handling import book
from keyboards.pagination_kb import create_pagination_kb
from keyboards.bookmarks import bookmarks_kb


router: Router = Router()


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    # Проверка регистрации пользователя
    if message.from_user.id not in users_dt:
        users_dt[message.from_user.id] = deepcopy(user_dict_template)

    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands=['begin']))
async def process_begin_command(message: Message):
    '''Начать читать с 1 страницы'''

    user_id = message.from_user.id
    users_dt[user_id]['page'] = 1
    text = book[users_dt[user_id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_kb(
                             page=users_dt[user_id]['page'],
                             len_book=len(book)))


@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    '''Продолжить чтение'''

    user_id = message.from_user.id
    text = book[users_dt[user_id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_kb(
                             page=users_dt[user_id]['page'],
                             len_book=len(book)))


@router.message(Command(commands=['save']))
async def process_save_command(message: Message):
    '''Функция сохраняет состояние'''

    save_progress()
    await message.answer(text=LEXICON_RU['save'])
    await message.answer_sticker(sticker=STICKERS['cool_duck'])


@router.callback_query(Text(text='backward'))
async def process_backward(callback: CallbackQuery):
    '''Переворачивание страницы <<назад>>'''

    user_id = callback.from_user.id
    users_dt[user_id]['page'] -= 1
    text = book[users_dt[user_id]['page']]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                         page=users_dt[user_id]['page'],
                                         len_book=len(book)))
    await callback.answer()


@router.callback_query(Text(text='forward'))
async def process_forward(callback: CallbackQuery):
    '''Переворачивание страницы <<вперед>>'''

    user_id = callback.from_user.id
    users_dt[user_id]['page'] += 1
    text = book[users_dt[user_id]['page']]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                         page=users_dt[user_id]['page'],
                                         len_book=len(book)))
    await callback.answer()


@router.message(Command(commands=['bookmarks']))
async def show_bookmarks(message: Message):
    '''Функция выводит закладки'''

    bookmarks = users_dt[message.from_user.id]['bookmarks']

    if bookmarks:
        await message.answer(text=LEXICON_RU['show_bm'],
                             reply_markup=bookmarks_kb(bookmarks))
    else:
        await message.answer(text=LEXICON_RU['no_bookmarks'])
        await message.answer_sticker(sticker=STICKERS['hmm'])
