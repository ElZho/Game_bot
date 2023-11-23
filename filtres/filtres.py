from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery, Update


class IsinGame(BaseFilter):
    def __init__(self, users) -> None:
        self.users = users

    async def __call__(self, message: Message| CallbackQuery) -> bool:
        return self.users[message.from_user.id]['in_game']


class IsUser(BaseFilter):
    def __init__(self, users) -> None:
        self.users = users

    async def __call__(self, message: Message| CallbackQuery) -> bool:
        return self.users[message.from_user.id]
