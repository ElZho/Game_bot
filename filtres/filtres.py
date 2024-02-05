from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery, Update


class IsinGame(BaseFilter):
    # check if user in game or not
    def __init__(self, users) -> None:
        self.users = users

    async def __call__(self, message: Message| CallbackQuery) -> bool:
        return self.users[message.from_user.id]['in_game']


class IsUser(BaseFilter):
    # check if user is in database or not
    def __init__(self, users) -> None:
        self.users = users

    async def __call__(self, message: Message| CallbackQuery) -> bool:
        return self.users[message.from_user.id]
