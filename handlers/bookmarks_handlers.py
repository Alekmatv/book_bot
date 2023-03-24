from aiogram.types import CallbackQuery
from aiogram.filters import Text
from aiogram import Router

from lexicon.lexicon import LEXICON_RU
from database.database import users_dt
from services.file_handling import book
from services.bookmarks_func import del_the_bookmark
from keyboards.pagination_kb import create_pagination_kb
from keyboards.bookmarks import (bookmarks_kb,
                                 edit_bookmarks_kb,
                                 deletion_confirmation)


router: Router = Router()


@router.callback_query(lambda x: '/' in x.data
                       and x.data.replace('/', '').isdigit())
async def create_bookmark(callback: CallbackQuery):
    '''Функция создает закладку'''

    bookmark: tuple = (users_dt[callback.from_user.id]['page'],
                       book[users_dt[callback.from_user.id]['page']][:25])

    users_dt[callback.from_user.id]['bookmarks'].add(
        bookmark)
    await callback.answer(text=LEXICON_RU['add'])


@router.callback_query(lambda x: isinstance(x.data, str) and x.data.isdigit())
async def open_the_bookmark(callback: CallbackQuery):
    '''Функция открывает выбранную закладку'''

    user_id = callback.from_user.id
    users_dt[user_id]['page'] = int(callback.data)
    text = book[users_dt[user_id]['page']]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                         page=users_dt[user_id]['page'],
                                         len_book=len(book)))


@router.callback_query(Text(text='come_back'))
async def come_back(callback: CallbackQuery):
    '''Функция отменяет выбор закладки и возвращает к чтению'''

    user_id = callback.from_user.id
    text = book[users_dt[user_id]['page']]
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                         page=users_dt[user_id]['page'],
                                         len_book=len(book)))


@router.callback_query(Text(text='edit_bm'))
async def edit_the_bookmarks(callback: CallbackQuery):
    '''Редактирование закладок'''

    bookmarks = users_dt[callback.from_user.id]['bookmarks']

    await callback.message.edit_text(text=LEXICON_RU['edit_bm'],
                                     reply_markup=edit_bookmarks_kb(bookmarks))


@router.callback_query(lambda x: 'del' in x.data and x.data[3:].isdigit())
async def delete_the_bookmark(callback: CallbackQuery):
    '''Функция выводит клавиатуру да/нет для подтверждения удаления'''

    await callback.message.edit_text(text=LEXICON_RU['yes_or_no'],
                                     reply_markup=deletion_confirmation(
        callback.data[3:]))


@router.callback_query(Text(text='cancel_del'))
async def back_to_bookmarks(callback: CallbackQuery):
    '''Функция заканчивает редактирование и возвращает список закладок'''

    bookmarks = users_dt[callback.from_user.id]['bookmarks']

    if bookmarks:
        await callback.message.edit_text(text=LEXICON_RU['show_bm'],
                                         reply_markup=bookmarks_kb(bookmarks))
    else:
        await come_back(callback)


@router.callback_query(lambda x: 'yes' in x.data and x.data[3:].isdigit())
async def yes_delete_bookmark(callback: CallbackQuery):
    '''Функция удаляет выбранную закладку'''

    bookmarks = users_dt[callback.from_user.id]['bookmarks']

    await del_the_bookmark(int(callback.data[3:]), bookmarks)

    if bookmarks:
        await callback.message.edit_text(text=LEXICON_RU['edit_bm'],
                                         reply_markup=edit_bookmarks_kb(
            bookmarks))
        await callback.answer(text=LEXICON_RU['del'])

    else:
        await come_back(callback)


@router.callback_query(Text(text='no'))
async def no_delete_bookmark(callback: CallbackQuery):
    '''Функция отменяет удаление закладки'''

    bookmarks = users_dt[callback.from_user.id]['bookmarks']

    await callback.message.edit_text(text=LEXICON_RU['edit_bm'],
                                     reply_markup=edit_bookmarks_kb(
        bookmarks))
