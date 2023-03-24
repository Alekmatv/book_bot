from aiogram.types import Message
from aiogram import Router

from lexicon.lexicon import LEXICON_RU, STICKERS

router: Router = Router()


@router.message()
async def process_other(message: Message):
    print(message)
    await message.answer(text=LEXICON_RU['other'])
    await message.answer_sticker(sticker=STICKERS['other'])
