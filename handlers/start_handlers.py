from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_YES_NO
from services.services import new_user, start_game
from filtres.filtres import IsUser
from database.first_model import users
from states.states import FSMInGame

router = Router()

# этот фильтр отбирает пользователей в игре
router.message.filter(StateFilter(default_state))


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    new_user(message.from_user.id)
    await message.answer(text=LEXICON_RU['/start'])
# @router.callback_query(CommandStart())
# async def process_start_command(callback: CallbackQuery):
#     new_user(callback.from_user.id)
#     await callback.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
# @router.callback_query(Command(commands='help'))
async def process_help_command(message: Message):
# async def process_help_command(callback: CallbackQuery):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /game
@router.message(Command(commands='game'), StateFilter(default_state))
async def process_game_command(message: Message, state: FSMContext):
    start_game(message.from_user.id)
    await message.answer(text=LEXICON_RU['yes'])
    await state.set_state(FSMInGame.wait_move)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.callback_query(F.data.in_(LEXICON_YES_NO.keys()), StateFilter(default_state))
async def process_yes_answer(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        start_game(callback.from_user.id)
    await callback.message.edit_text(text=LEXICON_RU[callback.data])
    await state.set_state(FSMInGame.wait_move)


# @router.message(F.text == LEXICON_RU['yes_button'], IsUser(users))
# async def process_yes_answer(message: Message):
#     start_game(message.from_user.id)
#     await message.answer(text=LEXICON_RU['yes'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
# @router.message(F.text == LEXICON_RU['no_button'], IsUser(users))
@router.callback_query(F.data.in_('no'), IsUser(users))
# async def process_no_answer(message: Message):
async def process_no_answer(callback: CallbackQuery):
    await callback.answer(text=LEXICON_RU['no'])
