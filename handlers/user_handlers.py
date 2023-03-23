from copy import deepcopy

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from aiogram import Router

from lexicon.lexicon import LEXICON_RU
from database.database import user_dict_template, users_dt
from services.file_handling import book
from keyboards.pagination_kb import create_pagination_kb

router: Router = Router()


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    print(message)
    # Проверка регистрации пользователя
    if message.from_user.id not in users_dt:
        users_dt[message.from_user.id] = deepcopy(user_dict_template)

    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands=['begin']))
async def process_begin_command(message: Message):
    user_id = message.from_user.id
    users_dt[user_id]['page'] = 1

    pages = f"{users_dt[user_id]['page']}/{len(book)}"
    text = book[users_dt[user_id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_kb(
                             'backward',
                             pages,
                             'forward'))


@router.callback_query(Text(text='backward'))
async def process_backward(callback: CallbackQuery):
    '''Переворачивание страницы <<назад>>'''
    user_id = callback.from_user.id
    users_dt[user_id]['page'] -= 1

    pages = f"{users_dt[user_id]['page']}/{len(book)}"
    text = book[users_dt[user_id]['page']]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                         'backward',
                                         pages,
                                         'forward'))
    await callback.answer()


@router.callback_query(Text(text='forward'))
async def process_forward(callback: CallbackQuery):
    '''Переворачивание страницы <<вперед>>'''
    user_id = callback.from_user.id
    users_dt[user_id]['page'] += 1

    pages = f"{users_dt[user_id]['page']}/{len(book)}"
    text = book[users_dt[user_id]['page']]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                         'backward',
                                         pages,
                                         'forward'))
    await callback.answer()
