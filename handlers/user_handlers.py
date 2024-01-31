from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import yes_no_kb, ask_result
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_INLINE_BUTTUNS
from services.services import (start_game, process_result,
                               check_users_number, write_history, get_users_moves)

from states.states import FSMInGame
from database.methods import add_user, create_game_report, count_games, get_game_statistic

router = Router()


# handler to catch command /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    add_user(message.from_user.id)
    await message.answer(text=LEXICON_RU['/start'])


# handler to catch command /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# handler to catch command /game
@router.message(Command(commands='game'), StateFilter(default_state))
async def process_game_command(message: Message, state: FSMContext):
    await state.set_state(default_state)
    new_game = start_game()
    await state.update_data(new_game)
    await message.answer(text=LEXICON_RU['yes'])
    await state.set_state(FSMInGame.wait_move)


# handler to catch if user wants to play
@router.callback_query(F.data.in_('yes'), StateFilter(default_state))
async def process_yes_answer(callback: CallbackQuery, state: FSMContext):
    new_game = start_game()
    await state.update_data(new_game)
    await callback.message.edit_text(text=LEXICON_RU[callback.data])
    await state.set_state(FSMInGame.wait_move)


# handler to catch if user refused to play the game
@router.callback_query(F.data.in_('no'), StateFilter(default_state))
async def process_no_answer(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['no'])


# handler to catch command "cansel", if user does not play the game
@router.message(Command(commands='cansel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['cansel_in_no_game'])


#  handler to catch command "cansel", if user plays the game 
# and stop user from defeat
@router.message(Command(commands='cansel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    data = await state.get_data()
    game = count_games(message.from_user.id) + 1
    create_game_report(message.from_user.id, game, 0, 1, data['attempts'])
    await message.answer(text=LEXICON_RU['cansel'])
    await state.clear()


# handler to catch command "Мои ходы" and shows history of users moves in corrent game
@router.message(Command(commands='my_moves'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    data = await state.get_data()
    history = get_users_moves(data['users_history'])
    text = LEXICON_RU['my_moves'] + history
    await message.answer(text)


# handler to catch command "Статистика" - statistics and shows statistics of users games
@router.message(Command(commands='stat'))
async def process_cancel_command(message: Message):
    result = get_game_statistic(message.from_user.id)
    if result:
        text = LEXICON_RU['statistics'].format(*result)
    else:
        text = LEXICON_RU['no statistic']
    await message.answer(text)


# handler to catch if user sends three-digits numbers
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
        number = data['source'][0]
        source = data['source'][1:]
        text = LEXICON_RU['inform_user'].format(b, c, ''.join(map(str, number)))
        await state.update_data(bots_number=''.join(map(str, number)), users_bulls_cow=str(b) + str(c), source=source,
                                users_history=write_history(message.text, b, c, data['users_history']))
        await message.answer(text, reply_markup=ask_result)
        await state.set_state(FSMInGame.wait_answer)


# handler to catch if user press 3-boll button.
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


# handler to catch users answer to bots current number
@router.callback_query(F.data.in_(LEXICON_INLINE_BUTTUNS.keys()), StateFilter(FSMInGame.wait_answer))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    # get bots number boll and cows
    b, c = list(map(int, list(callback.data)))
    # get previously saved data
    data = await state.get_data()
    # write moves history
    history = write_history(data['bots_number'], b, c, data['history'])

    # send data to memory storage
    source, k, cow = process_result(b, c, data['source'], history, list(map(int, list(data['bots_number']))), data['k'],
                                    data['cow'])
    # update data in memory storage
    await state.update_data(source=source, bots_bulls_cow=callback.data, history=history, k=k, cow=cow)
    # make text for massage
    text = LEXICON_RU['answer'].format(data['attempts'], data['users_number'], *list(data['users_bulls_cow']),
                                       data['bots_number'], b, c)
    # check if user guessed number or not
    if data['users_bulls_cow'] == '30':
        game = count_games(callback.from_user.id) + 1
        create_game_report(callback.from_user.id, game, 1, 0, data['attempts'])
        # update text in massege if user guessed number.
        await callback.message.edit_text(text+LEXICON_RU['user_guess'], reply_markup=yes_no_kb)
        await state.clear()
    else:
        # update text in massege if user does not guess
        await callback.message.edit_text(text+LEXICON_RU['your_move'])
        await state.set_state(FSMInGame.wait_move)
