from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
# from aiogram import types

from keyboards.keyboards import yes_no_kb, ask_result
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_INLINE_BUTTUNS, LEXICON_YES_NO
from services.services import (new_user, start_game, press_cansel, guess_number, process_result, result_3_bulls)
# from filtres.filtres import IsinGame
# from database.first_model import users
from states.states import FSMInGame

router = Router()

# этот фильтр отбирает пользователей в игре
router.message.filter()


router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    new_user(message.from_user.id)
    await message.answer(text=LEXICON_RU['/start'])


# @router.message(Command(commands='del_menu'))
# async def remove_kb(message: types.Message):
#     await message.answer(
#         text='Удаляю клавиатуру',
#         reply_markup=types.ReplyKeyboardRemove())


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /game
@router.message(Command(commands='game'), StateFilter(default_state))
async def process_game_command(message: Message, state: FSMContext):
    start_game(message.from_user.id)
    await message.answer(text=LEXICON_RU['yes'])
    await state.set_state(FSMInGame.wait_move)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.callback_query(F.data.in_('yes'), StateFilter(default_state))
async def process_yes_answer(callback: CallbackQuery, state: FSMContext):
    start_game(callback.from_user.id)
    await callback.message.edit_text(text=LEXICON_RU[callback.data])
    await state.set_state(FSMInGame.wait_move)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.callback_query(F.data.in_('no'), StateFilter(default_state))
async def process_no_answer(callback: CallbackQuery, state: FSMContext):
    print(await state.get_state())
    await callback.answer(text=LEXICON_RU['no'])


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cansel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['cansel_in_no_game'])


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cansel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    key = press_cansel(message.from_user.id)
    print(await state.get_state())
    await message.answer(text=LEXICON_RU[key])
    await state.clear()


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 100 до 1000
@router.message(lambda x: x.text and x.text.isdigit() and len(x.text) == 3, StateFilter(FSMInGame.wait_move))
async def process_numbers_answer(message: Message, state: FSMContext):
    await state.update_data(users_number=message.text)
    key = guess_number(message.from_user.id, message.text)
    if any(map(lambda x: isinstance(x, (int, list)), key)):
        text = LEXICON_RU[key[0]].format(key[1], key[2], ''.join(map(str, key[3])))
    else:
        text = LEXICON_RU[key[0]]
    await message.answer(text, reply_markup=ask_result)
    await state.set_state(FSMInGame.wait_answer)


@router.callback_query(F.data.in_('30'), StateFilter(FSMInGame.wait_answer))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    text = LEXICON_RU[result_3_bulls(callback.from_user.id)]
    await state.update_data(bots_bulls_cow=callback.data)
    print(await state.get_data())
    print(await state.get_state())
    await callback.message.edit_text(text, reply_markup=yes_no_kb)
    await state.clear()


@router.callback_query(F.data.in_(LEXICON_INLINE_BUTTUNS.keys()), StateFilter(FSMInGame.wait_answer))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    b, c = list(map(int, list(callback.data)))
    result = process_result(b, c, callback.from_user.id)
    text = LEXICON_RU['answer'].format(*result[0]) + LEXICON_RU[result[1]]
    await state.update_data(bots_bulls_cow=callback.data)
    print(await state.get_data())
    print(await state.get_state())
    await callback.message.edit_text(text)
    if LEXICON_RU[result[1]] == 'user_guess':
        await state.clear()
    else:
        await state.set_state(FSMInGame.wait_move)
