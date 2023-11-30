import random
from itertools import permutations
from typing import Any


# Добавляем нового пользователя
def _new_game(secret_number: list, source: list) -> dict:
    return dict(secret_number=secret_number, attempts=0,
                history={'3b0c': [], '1b2c': [], '0b3c': [], '2b0c': [], '0b2c': [], '1b1c': [], '1b0c': [],
                         '0b1c': []}, k=3, source=source, cow=[])


def _drop_pars(sample, item):
    return list(filter(lambda x: not any(
        (item[0] in x and item[1] in x, item[0] in x and item[2] in x, item[1] in x and item[2] in x)), sample))


def _keep_pars(example, new_var):
    return list(filter(lambda x: any([new_var[0] in x and new_var[1] in x,
                                      new_var[0] in x and new_var[2] in x,
                                      new_var[1] in x and new_var[2] in x]), example))


# пишем результат в историю
def write_history(number: list, b: int, c: int, history: dict) -> dict:
    key = f'{b}b{c}c'
    history[key].append(list(map(int, list(number))))
    return history


def _check_source(example: list, new_var: list, b: int, c: int, cow=None) -> list:
    print('example - ', example, 'cow - ', cow, 'new_var - ', new_var)
    if not cow:
        cow = []
    if cow:
        example = list(filter(lambda x: all(i in x for i in cow), example))
    if b + c == 3:
        print('b + c == 3')
        # контроль на то, чтобы все цифры были в числе
        example = list(filter(lambda x: all([i in x for i in new_var]), example))
        # контроль на то, чтобы убрать использованный вариант
        example = list(filter(lambda x: list(x) != new_var, example))
    elif b == 2 and c == 0:
        print('b == 2 and c == 0')
        example = list(filter(lambda x: any([new_var[0] == x[0] and new_var[1] == x[1],
                                             new_var[0] == x[0] and new_var[2] == x[2],
                                             new_var[1] == x[1] and new_var[2] == x[2]]), example))
    elif b == 1 and c == 0:
        print('b == 1 and c == 0')
        # контроль на то, чтобы цифры из варианта с быками были на своем месте
        example = list(filter(lambda x: all([x[i] == new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))
    # контроль на то, чтобы цифры из варианта с коровами не были на своем месте
    elif b == 0 and c == 2:
        print('b == 0 and c == 2')
        example = _keep_pars(example, new_var)

        example = list(filter(lambda x: all([x[i] != new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))
    elif b == 0 and c > 0:
        print('b == 0 and c > 0')
        example = list(filter(lambda x: all([x[i] != new_var[i] for i in range(3)
                                             if new_var[i] in x]), example))
    # контроль на то, чтобы в вариантах присутствовали 2 цифры из варианта, где было 2 правильные цифры
    elif b + c == 2:
        print('b + c == 2')
        example = _keep_pars(example, new_var)
        # контроль на то, чтобы все 3 цифры не входили в варианты
        example = list(filter(lambda x: not all([i in x for i in new_var]), example))

    if b + c == 1:
        print('b + c == 1')
        # контроль, чтобы цифры из варианта с 1 правильной цифрой не встречались в одном варианте
        example = _drop_pars(example, new_var)
    # удаляем уже имеющиеся экзепляры
    if b + c < 3:
        print('b + c < 3')
        # контроль на то, чтобы варианты с тем же набором цифр не повторялись
        example = list(filter(lambda x: sorted(x) != sorted(new_var), example))

    example = list(filter(lambda x: x[0] != 0, example))
    print('source - ', example)
    return example


# набор источника
def _collect_source(history: dict, cow=None) -> list:
    if not cow:
        cow = []
    source = []
    if cow:
        source.extend(cow)
    for val in history.values():
        if val:
            for v in val:
                source.extend(v)
    source = list(set(source))
    source = list(permutations(source, 3))

    for k, val in history.items():
        if val:
            for v in val:
                source = _check_source(source, v, int(k[0]), int(k[2]), cow)
    return source


# Отработка нажатия кнопки Старт игры. Генерим чмсло, загаданное ботом. Генерим источник для отгадывания чисел ботом.
# Устанавливаем все счетчики и накопители на начальные значения
def start_game() -> dict:
    def get_random_number() -> list:
        sample = list(permutations(list(range(0, 10)), 3))
        sample = list(filter(lambda x: x[0] != 0, sample))
        for it in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            sample = _drop_pars(sample, it)
        random.shuffle(sample)
        return next(iter(sample))

    secret_number = get_random_number()
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
# def process_result(b, c, user_id) -> tuple[list[list[str | list | Any] | str], Any]:
def process_result(b: int, c: int, source: list, history: dict, bots_current_number: list, k: int, cow=None) -> tuple[
        list[list[str | list | Any] | str], Any]:
    if not cow:
        cow = []
    if b + c == 0:  # если в наборе нет ни быков ни коров, чистим источник от вариантов с этими цифрами
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
