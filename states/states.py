from aiogram.fsm.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMInGame(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    wait_move = State()        # Состояние ожидания хода пользоавтеля
    wait_answer = State()         # Состояние ожидания ответа пользователя на ход бота