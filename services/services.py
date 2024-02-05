import random
from itertools import permutations

from lexicon.lexicon_ru import LEXICON_RU


# create a dict for new game
def _new_game(secret_number: list, source: list) -> dict:
    return dict(secret_number=secret_number, attempts=0,
                history={'3b0c': [], '1b2c': [], '0b3c': [], '2b0c': [], '0b2c': [], '1b1c': [], '1b0c': [],
                         '0b1c': [], '0b0c': []}, k=3, source=source, cow=[], users_history={'3b0c': [], '1b2c': [],
                                                                                             '0b3c': [], '2b0c': [],
                                                                                             '0b2c': [], '1b1c': [],
                                                                                             '1b0c': [], '0b1c': [],
                                                                                             '0b0c': []})


def _drop_pars(sample, item):
    ''' This func delete wrong set of digits, where are 2 digits from set, where just 1 digit is right'''
    return list(filter(lambda x: not any(
        (item[0] in x and item[1] in x, item[0] in x and item[2] in x, item[1] in x and item[2] in x)), sample))


def _keep_pars(example, new_var):
    ''' This func delete wrong set of digits, where are not 2 digits from set, where 2 digit is right'''
    return list(filter(lambda x: any([new_var[0] in x and new_var[1] in x,
                                      new_var[0] in x and new_var[2] in x,
                                      new_var[1] in x and new_var[2] in x]), example))


# write result in game's history
def write_history(number: str, b: int, c: int, history: dict) -> dict:
    key = f'{b}b{c}c'
    history[key].append(list(map(int, list(number))))
    return history


def _check_source(example: list, new_var: list, b: int, c: int, cow=None) -> list:
    ''' This func process source of sets depends of set bot declare and result of this bot's move. 
    Delets wrong sets'''
    if not cow:
        cow = []
    # If there is a cow, then check, that this digit is in all sets in source. Cow is a necessarily in set.
    if cow:
        example = list(filter(lambda x: all(i in x for i in cow), example))

    # Check if we know all right digits, all that digits should be in set. Sets that not have all right digit should be deleted
    if b + c == 3:
        # check that all digit in set
        example = list(filter(lambda x: all([i in x for i in new_var]), example))
        # check if used set is deleted
        example = list(filter(lambda x: list(x) != new_var, example))

    # If 2 bulls in declared set, delete sets, where digits from this set are in right positions like in declared set
    elif b == 2 and c == 0:
        example = list(filter(lambda x: any([new_var[0] == x[0] and new_var[1] == x[1],
                                             new_var[0] == x[0] and new_var[2] == x[2],
                                             new_var[1] == x[1] and new_var[2] == x[2]]), example))

    # Delete sets, which not response declared set with 1 bull
    elif b == 1 and c == 0:
        # check right position of each digits in set
        example = list(filter(lambda x: all([x[i] == new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))

    # check for declared set with 2 cows. All digits not in position like in declared set
    elif b == 0 and c == 2:
        # delete all set, where not 2 digits from set with 2 cows
        example = _keep_pars(example, new_var)
        # delete all set, where digits on positions like in set with 2 cows
        example = list(filter(lambda x: all([x[i] != new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))
    # process set, which consists of cows
    elif b == 0 and c > 0:
        example = list(filter(lambda x: all([x[i] != new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))

    # check that sets conteins 2 digits wrom set with 2 right digits
    elif b + c == 2:
        # delete all set, which do not contein 2 digit from set with 2 right digits
        example = _keep_pars(example, new_var)
        # delete all sets, which conteins 3 digits from set wich 2 right digits
        example = list(filter(lambda x: not all([i in x for i in new_var]), example))

    # delete sets that contains more that 1 digit from set wich 1 right digit 
    if b + c == 1:
        example = _drop_pars(example, new_var)

    # delete all declared sets
    if b + c < 3:
        example = list(filter(lambda x: sorted(x) != sorted(new_var), example))
    # delete all sets where 0 is on first position
    example = list(filter(lambda x: x[0] != 0, example))

    return example


# create set's source
def _collect_source(history: dict, cow=None) -> list:
    ''' This func creates a source of sets from digits from history after all digits from 0 to 9 where declared'''
    if not cow:
        cow = []
    source = []

    # Если названы 3 варианта и осталась одна свободная позиция и одно не названное число - это число точно корова
    # и это число точно должно быть во всех вариантах
    if cow:
        source.extend(cow)

    # Перебираем историю и набираем цифры, из которых формировать варианты
    for key, val in history.items():
        if key != '0b0c' and val:
            for v in val:
                source.extend(v)
    # удаляем дубли
    source = list(set(source))

    # формируем варианты
    source = list(permutations(source, 3))

    # удаляем варианты, несоответствующие истории
    for key, val in history.items():
        if key != '0b0c' and val:
            for v in val:
                source = _check_source(source, v, int(key[0]), int(key[2]), cow)
    return source


# Отработка нажатия кнопки Старт игры. Генерим чмсло, загаданное ботом. Генерим источник для отгадывания чисел ботом.
# Устанавливаем все счетчики и накопители на начальные значения
def start_game() -> dict:
    ''' Эта функция срабатывает на стар игры и формирует "загаданное" ботом число'''

    def get_random_number() -> list:
        ''' Эта функция генерит загаданное число'''
        sample = list(permutations(list(range(0, 10)), 3))
        sample = list(filter(lambda x: x[0] != 0, sample))
        for it in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            sample = _drop_pars(sample, it)
        random.shuffle(sample)
        return next(iter(sample))

    # сохраняем сгенерированное число
    secret_number = get_random_number()

    # формируем источник вариантов для начала перебора вариантов, до нахождения 3-х цифр.
    source = list(range(0, 10))
    random.shuffle(source)
    source = [source[:3], source[3:6], source[6:9], source[9:10]]
    for i in range(4):
        while source[i][0] == 0:
            random.shuffle(source[i])
    return _new_game(secret_number, source)


# проверяем номер пользователя на соответствие загаданному числу
def check_users_number(number, secret_number):
    b = sum([number[i] == secret_number[i] for i in range(3)])
    c = sum([number[i] in secret_number for i in range(3)]) - b
    return b, c


# запись в историю обработка источника, который генерит числа
def process_result(b: int, c: int, source: list, history: dict, bots_current_number: list, k: int, cow=None) -> tuple[
    list, int, int]:
    '''Функция обрабатывает результат по ответу пользователя на вариант числа бота'''
    if not cow:
        cow = []
    # если в наборе нет ни быков ни коров, чистим источник от вариантов с этими цифрами
    if b + c == 0:
        source = list(filter(lambda x: all([i not in x for i in bots_current_number]), source))

    # если еще не набран источник формирования числа
    if k > 0:
        k -= (b + c)  # уменьшаем количество знаков, которое мы еще не набрали
        source = list(filter(lambda x: sorted(x) != sorted(bots_current_number), source))
        # если все тройки перебраны, а одна позиция осталась, то пишем оставшуюся цифру, во все позиции включая
        # позицию для обязательного использования
        if k == 1 and len(source) == 1:
            cow = source[0]
            k = 0
        if k == 0:  # если перебраны 10 цифр формируем источник заново
            source = _collect_source(history, cow)

    # если уже источник полностью сформирован
    else:
        source = _check_source(source, bots_current_number, b, c, cow)
        random.shuffle(source)  # перемешиваем источник
    return source, k, cow


def get_users_moves(history: dict) -> str:
    ''' Функция фурмирует отчет о ходах пользователя в последней игре'''
    text = ''
    for keys, vals in history.items():
        if vals:
            for val in vals:
                text += LEXICON_RU['my_move_schema'].format(''.join(map(str, val)), keys[0], keys[2])
    return text
