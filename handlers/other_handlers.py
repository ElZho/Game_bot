from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon_ru import LEXICON_RU

router = Router()


# handler for the message, which do not catched other handlers 
@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])
