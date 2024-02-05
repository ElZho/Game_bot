from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from lexicon.lexicon_ru import LEXICON_INLINE_BUTTUNS, LEXICON_YES_NO


# initialize a yes/no builder
yes_no_kb_builder = InlineKeyboardBuilder()

# initialize the list of buttons
y_n_buttons: list[InlineKeyboardButton] = []

# create the "yes" and "no" 
for button in LEXICON_YES_NO:
    y_n_buttons.append(InlineKeyboardButton(
        text=LEXICON_YES_NO[button] if button in LEXICON_YES_NO else button,
        callback_data=button))

# add buttons into builder. width=2
yes_no_kb_builder.row(*y_n_buttons, width=2)

# create the buttons "let's play" and "don't want"
yes_no_kb = yes_no_kb_builder.as_markup()

# initialize play buttons builder
kb_builder = InlineKeyboardBuilder()

# initialize the list of buttons
buttons: list[InlineKeyboardButton] = []

# create game's buttons
for button in LEXICON_INLINE_BUTTUNS:
    buttons.append(InlineKeyboardButton(
        text=LEXICON_INLINE_BUTTUNS[button] if button in LEXICON_INLINE_BUTTUNS else button,
        callback_data=button))

# create game's buttons keyboard
kb_builder.row(*buttons, width=3)
kb_builder.adjust(3, 2, 3)
ask_result = kb_builder.as_markup()
