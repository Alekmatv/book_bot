from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from lexicon.lexicon import LEXICON_RU

router: Router = Router()


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
