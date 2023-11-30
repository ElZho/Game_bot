from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from lexicon.lexicon_ru import LEXICON_INLINE_BUTTUNS, LEXICON_YES_NO

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Инициализируем билдер
yes_no_kb_builder = InlineKeyboardBuilder()

# Инициализируем список для кнопок
y_n_buttons: list[InlineKeyboardButton] = []

# Создаем кнопки с ответами согласия и отказа
for button in LEXICON_YES_NO:
    y_n_buttons.append(InlineKeyboardButton(
        text=LEXICON_YES_NO[button] if button in LEXICON_YES_NO else button,
        callback_data=button))


# button_yes = InlineKeyboardButton(text=LEXICON_RU['yes_button'])
# button_no = InlineKeyboardButton(text=LEXICON_RU['no_button'])

# # Инициализируем билдер для клавиатуры с кнопками "Давай" и "Не хочу!"
# yes_no_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
yes_no_kb_builder.row(*y_n_buttons, width=2)
# yes_no_kb_builder.row(button_yes, button_no, width=2)

# Создаем клавиатуру с кнопками "Давай!" и "Не хочу!"
# yes_no_kb: ReplyKeyboardMarkup = yes_no_kb_builder.as_markup(resize_keyboard=True)
yes_no_kb = yes_no_kb_builder.as_markup()

# ------- Создаем игровую клавиатуру без использования билдера -------


# Инициализируем билдер
kb_builder = InlineKeyboardBuilder()

# Инициализируем список для кнопок
buttons: list[InlineKeyboardButton] = []

# Создаем кнопки игровой клавиатуры
for button in LEXICON_INLINE_BUTTUNS:
    buttons.append(InlineKeyboardButton(
        text=LEXICON_INLINE_BUTTUNS[button] if button in LEXICON_INLINE_BUTTUNS else button,
        callback_data=button))
#
# result_buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_RU['30']),
#                                        InlineKeyboardButton(text=LEXICON_RU['20']),
#                                        InlineKeyboardButton(text=LEXICON_RU['10']),
#                                        InlineKeyboardButton(text=LEXICON_RU['12']),
#                                        InlineKeyboardButton(text=LEXICON_RU['11']),
#                                        InlineKeyboardButton(text=LEXICON_RU['03']),
#                                        InlineKeyboardButton(text=LEXICON_RU['02']),
#                                        InlineKeyboardButton(text=LEXICON_RU['01']),
#                                        InlineKeyboardButton(text=LEXICON_RU['00'])]


# Создаем клавиатуру с кнопками результата ответа
kb_builder.row(*buttons, width=3)
# kb_builder.add(*result_buttons)
kb_builder.adjust(3, 2, 3)
ask_result = kb_builder.as_markup()
