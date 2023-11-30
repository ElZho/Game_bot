from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import yes_no_kb, ask_result
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_INLINE_BUTTUNS
from services.services import (start_game, process_result,
                               check_users_number, write_history)

from states.states import FSMInGame
from database.methods import add_user, create_game_report, count_games

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    add_user(message.from_user.id)
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /game
@router.message(Command(commands='game'), StateFilter(default_state))
async def process_game_command(message: Message, state: FSMContext):
    await state.set_state(default_state)
    new_game = start_game()
    # await state.update_data(attempts=0, source=source, k=3, secret_number=secret_number, history={'3b0c': [],
    #                                                                                               '1b2c': [],
    #                                                                                               '0b3c': [],
    #                                                                                               '2b0c': [],
    #                                                                                               '0b2c': [],
    #                                                                                               '1b1c': [],
    #                                                                                               '1b0c': [],
    #                                                                                               '0b1c': []})
    await state.update_data(new_game)
    await message.answer(text=LEXICON_RU['yes'])
    await state.set_state(FSMInGame.wait_move)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.callback_query(F.data.in_('yes'), StateFilter(default_state))
async def process_yes_answer(callback: CallbackQuery, state: FSMContext):
    new_game = start_game()
    # await state.update_data(attempts=0, source=source, k=3, secret_number=secret_number, history={'3b0c': [],
    #                                                                                               '1b2c': [],
    #                                                                                               '0b3c': [],
    #                                                                                               '2b0c': [],
    #                                                                                               '0b2c': [],
    #                                                                                               '1b1c': [],
    #                                                                                               '1b0c': [],
    #                                                                                               '0b1c': []})
    await state.update_data(new_game)
    await callback.message.edit_text(text=LEXICON_RU[callback.data])
    await state.set_state(FSMInGame.wait_move)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.callback_query(F.data.in_('no'), StateFilter(default_state))
async def process_no_answer(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['no'])


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cansel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['cansel_in_no_game'])


# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cansel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['cansel'])
    await state.clear()


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 100 до 1000
@router.message(lambda x: x.text and x.text.isdigit() and len(x.text) == 3, StateFilter(FSMInGame.wait_move))
async def process_numbers_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(users_number=message.text, attempts=data['attempts'] + 1)
    b, c = check_users_number(tuple(map(int, list(message.text))), data['secret_number'])
    if len(data['source']) == 0:
        text = LEXICON_RU['cheat']
        await message.answer(text)
        await state.clear()
    else:
        if len(data['source']) > 1:
            number = data['source'][0]
            source = data['source'][1:]
        else:
            number = data['source'][0]
            source = []
        text = LEXICON_RU['inform_user'].format(b, c, ''.join(map(str, number)))
        await state.update_data(bots_number=''.join(map(str, number)), users_bulls_cow=str(b) + str(c), source=source)
        await message.answer(text, reply_markup=ask_result)
        await state.set_state(FSMInGame.wait_answer)


@router.callback_query(F.data.in_('30'), StateFilter(FSMInGame.wait_answer))
async def three_bull_buttons_press(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['users_bulls_cow'] == '30':
        win = 1
        key = 'both_wins'
    else:
        win = 0
        key = 'bot_wins'
    game = count_games(callback.from_user.id) + 1
    create_game_report(callback.from_user.id, game, win, 1, data['attempts'])
    text = LEXICON_RU[key]
    await callback.message.edit_text(text, reply_markup=yes_no_kb)
    await state.clear()


@router.callback_query(F.data.in_(LEXICON_INLINE_BUTTUNS.keys()), StateFilter(FSMInGame.wait_answer))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    b, c = list(map(int, list(callback.data)))
    data = await state.get_data()
    if b + c > 0:
        history = write_history(data['bots_number'], b, c, data['history'])
    else:
        history = data['history']
    source, k, cow = process_result(b, c, data['source'], history, list(map(int, list(data['bots_number']))), data['k'],
                                    data['cow'])
    await state.update_data(source=source, bots_bulls_cow=callback.data, history=history, k=k, cow=cow)
    text = LEXICON_RU['answer'].format(data['attempts'], data['users_number'], *list(data['users_bulls_cow']),
                                       data['bots_number'], b, c )
    if data['users_bulls_cow'] == '30':
        game = count_games(callback.from_user.id) + 1
        create_game_report(callback.from_user.id, game, 1, 0, data['attempts'])
        await callback.message.edit_text(text+LEXICON_RU['user_guess'], reply_markup=yes_no_kb)
        await state.clear()
    else:
        await callback.message.edit_text(text+LEXICON_RU['your_move'])
        await state.set_state(FSMInGame.wait_move)
