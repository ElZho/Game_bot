from aiogram.fsm.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMInGame(StatesGroup):
    # состояние пользователя в игре. Сообщает чей ход ожидается
    wait_move = State()        # Состояние ожидания хода пользоавтеля
    wait_answer = State()         # Состояние ожидания ответа пользователя на ход бота
