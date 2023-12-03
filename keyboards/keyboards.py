from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from lexicon.lexicon_ru import LEXICON_INLINE_BUTTUNS, LEXICON_YES_NO


# Инициализируем билдер
yes_no_kb_builder = InlineKeyboardBuilder()

# Инициализируем список для кнопок
y_n_buttons: list[InlineKeyboardButton] = []

# Создаем кнопки с ответами согласия и отказа
for button in LEXICON_YES_NO:
    y_n_buttons.append(InlineKeyboardButton(
        text=LEXICON_YES_NO[button] if button in LEXICON_YES_NO else button,
        callback_data=button))

# Добавляем кнопки в билдер с аргументом width=2
yes_no_kb_builder.row(*y_n_buttons, width=2)

# Создаем клавиатуру с кнопками "Давай!" и "Не хочу!"
yes_no_kb = yes_no_kb_builder.as_markup()

# Инициализируем билдер
kb_builder = InlineKeyboardBuilder()

# Инициализируем список для кнопок
buttons: list[InlineKeyboardButton] = []

# Создаем кнопки игровой клавиатуры
for button in LEXICON_INLINE_BUTTUNS:
    buttons.append(InlineKeyboardButton(
        text=LEXICON_INLINE_BUTTUNS[button] if button in LEXICON_INLINE_BUTTUNS else button,
        callback_data=button))

# Создаем клавиатуру с кнопками результата ответа
kb_builder.row(*buttons, width=3)
kb_builder.adjust(3, 2, 3)
ask_result = kb_builder.as_markup()
