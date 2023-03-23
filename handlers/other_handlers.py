from aiogram.types import Message
from aiogram import Router

from lexicon.lexicon import LEXICON_RU

router: Router = Router()


@router.message()
async def process_other(message: Message):
    await message.answer(text=LEXICON_RU['other'])
