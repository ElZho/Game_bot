import random
from itertools import permutations

from database.first_model import users


# Добавляем нового пользователя
def new_user(user_id):
    if user_id not in users:
        users[user_id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0,
            'defeats': 0,
            'bulls': 0,
            'cows': 0,
            "history": {'3b0c': [], '1b2c': [], '0b3c': [], '2b0c': [], '0b2c': [], '1b1c': [], '1b0c': [], '0b1c': []},
            "cow": [],
            "k": 3,
            'source': [],
            'users_current_number': None,
            'bots_current_number': None
        }


def _drop_pars(sample, item):

    return list(filter(lambda x: not any(
        (item[0] in x and item[1] in x, item[0] in x and item[2] in x, item[1] in x and item[2] in x)), sample))


# Обрабатываем победу
def _win(user_id: int, winner: str = 'user') -> None:
    users[user_id]['in_game'] = False
    users[user_id]['total_games'] += 1
    if winner == 'bot':
        users[user_id]['defeats'] += 1
    elif winner == 'both':
        users[user_id]['wins'] += 1
        users[user_id]['defeats'] += 1
    else:
        users[user_id]['wins'] += 1


# пишем результат в историю
def _write_history(user_id: int, number: list, b: int, c: int) -> None:
    key = f'{b}b{c}c'
    users[user_id]['history'][key].append(number)


def _check_source(example: list, new_var: list, b: int, c: int, cow) -> list:
    if cow:
        example = list(filter(lambda x: all(c in x for c in cow), example))
    if b + c == 3:
        # контроль на то, чтобы все цифры были в числе
        example = list(filter(lambda x: all([i in x for i in new_var]), example))

        # контроль на то, чтобы убрать использованный вариант
        example = list(filter(lambda x: list(x) != new_var, example))

    elif b > 0 and c == 0:
        # контроль на то, чтобы цифры из варианта с быками были на своем месте
        example = list(filter(lambda x: all([x[i] == new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))
    # контроль на то, чтобы цифры из варианта с коровами не были на своем месте
    elif b == 0 and c > 0:
        example = list(filter(lambda x: all([x[i] != new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))
    # контроль на то, чтобы в вариантах присутствовали 2 цифры из варианта, где было 2 правильные цифры
    elif b + c == 2:

        example = list(filter(lambda x: any([new_var[0] in x and new_var[1] in x,
                                             new_var[0] in x and new_var[2] in x,
                                             new_var[1] in x and new_var[2] in x]), example))
        # контроль на то, чтобы все 3 цифры не входили в варианты

        example = list(filter(lambda x: not all([i in x for i in new_var]), example))

    if b + c == 1:
        # контроль, чтобы цифры из варианта с 1 правильной цифрой не встречались в одном варианте
        example = _drop_pars(example, new_var)
    # удаляем уже имеющиеся экзепляры
    if b + c < 3:
        # контроль на то, чтобы варианты с тем же набором цифр не повторялись
        example = list(filter(lambda x: sorted(x) != sorted(new_var), example))

    example = list(filter(lambda x: x[0] != 0, example))
    return example


# набор источника
def _collect_source(cow: int, history: dict) -> list:
    source = []
    if cow:
        source.extend(cow)
    for val in history.values():
        if val:
            for v in val:
                source.extend(v)

    source = list(set(source))
    source = list()

    for k, val in history.items():
        if val:
            for v in val:
                source = _check_source(source, v, int(k[0]), int(k[2]), cow)
    return source


# Реакция на кнопку отмены игры. Увеличиваем на 1 кол-во сыгранных игр
def press_cansel(user_id):
    users[user_id]['total_games'] += 1
    return 'cansel'


# Отработка нажатия кнопки Старт игры. Генерим чмсло, загаданное ботом. Генерим источник для отгадывания чисел ботом.
# Устанавливаем все счетчики и накопители на начальные значения
def start_game(user_id) -> None:
    def get_random_number() -> list:
        sample = list(permutations(list(range(0, 10)), 3))
        sample = list(filter(lambda x: x[0] != 0, sample))
        for it in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            sample = _drop_pars(sample, it)
        random.shuffle(sample)
        return next(iter(sample))

    users[user_id]['in_game'] = True
    users[user_id]['secret_number'] = get_random_number()
    users[user_id]['attempts'] = 0
    source = list(range(0, 10))
    random.shuffle(source)
    users[user_id]["history"] = {'3b0c': [], '1b2c': [], '0b3c': [], '2b0c': [], '0b2c': [], '1b1c': [], '1b0c': [],
                                 '0b1c': []}
    users[user_id]['source'] = [source[:3], source[3:6], source[6:9], source[9:10]]
    users[user_id]['cow'] = []
    users[user_id]["k"] = 3
        # print(users[user_id]['secret_number'])


# реакция на отправку пользователем очередного числа
def guess_number(user_id, number) -> list():
    users[user_id]['users_current_number'] = list(number)
    user_number = list(map(int, users[user_id]['users_current_number']))
    users[user_id]['bulls'] = 0
    users[user_id]['cows'] = 0
    users[user_id]['attempts'] += 1

    for i, n in enumerate(user_number):
        if n == users[user_id]['secret_number'][i]:
            users[user_id]['bulls'] += 1
        elif n in users[user_id]['secret_number']:
            users[user_id]['cows'] += 1
    text_mess = ['inform_user', users[user_id]['bulls'], users[user_id]['cows']]
    if users[user_id]['k'] > 0:
        users[user_id]['bots_current_number'] = next(
            iter(users[user_id]['source']))  # выдаем очередной номер
        if users[user_id]['bots_current_number'][0] == 0:
            random.shuffle(users[user_id]['bots_current_number'])
        text_mess.append(users[user_id]['bots_current_number'])
    else:
        if len(users[user_id]['source']) == 0:  # проверяем что источник не пустой
            text_mess.append('cheat')
            _win(user_id)
        else:
            users[user_id]['bots_current_number'] = next(iter(users[user_id]['source']))  # выдаем очередной номер
            text_mess.append(users[user_id]['bots_current_number'])
    return text_mess


# если угадано число
def result_3_bulls(user_id) -> str:
    # если 3 быка определяем победителя
    if tuple(map(int, users[user_id]['users_current_number'])) == users[user_id]['secret_number']:
        _win(user_id, 'both')
        return 'both_wins'
    else:
        _win(user_id, 'bot')
        return 'bot_wins'


# запись в историю обработка источника, который генерит числа
def process_result(b, c, user_id) -> list[list[str | int | int] | str]:
    text_mess = []
    if b + c == 0:  # если в наборе нет ни быков ни коров, чистим источник от вариантов с этими цифрами
        users[user_id]['source'] = list(
            filter(lambda x: all([i not in x for i in users[user_id]['bots_current_number']]),
                   users[user_id]['source']))

    # обработка результата
    if b + c > 0:  # если попытка результативна пишем в историю
        _write_history(user_id, users[user_id]['bots_current_number'], b, c)

    # если еще не набран источник формирования числа
    if users[user_id]['k'] > 0:
        users[user_id]['k'] -= (b + c)  # уменьшаем количество знаков, которое мы еще не набрали
        source = users[user_id]['source']
        new_try = users[user_id]['bots_current_number']
        users[user_id]['source'] = list(filter(lambda x: sorted(x) != sorted(new_try), source))
        # если все тройки перебраны, а одна позиция осталась, то пишем оставшуюся цифру, во все позиции включая
        # позицию для обязательного использования
        if users[user_id]['k'] == 1 and len(users[user_id]['source']) == 1:
            users[user_id]['cow'].extend(users[user_id]['source'][0])
            users[user_id]['k'] = 0
        if users[user_id]['k'] == 0:  # если перебраны 10 цифр формируем источник заново
            users[user_id]['source'] = _collect_source(users[user_id]['cow'], users[user_id]['history'])
    # если уже источник полностью сформирован
    else:
        source = users[user_id]['source']
        new_try = users[user_id]['bots_current_number']
        users[user_id]['source'] = _check_source(source, new_try, b, c, users[user_id]['cow'])
        random.shuffle(users[user_id]['source'])  # перемешиваем источник

    text_mess.append([users[user_id]["attempts"], "".join(map(str, users[user_id]["users_current_number"])),
                      users[user_id]["bulls"], users[user_id]["cows"],
                      "".join(map(str, users[user_id]["bots_current_number"])), b, c])

    if tuple(map(int, users[user_id]['users_current_number'])) == users[user_id]['secret_number']:
        _win(user_id, 'user')
        text_mess.append('user_guess')
    else:
        text_mess.append('your_move')
    return text_mess
