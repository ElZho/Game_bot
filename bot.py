import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu


# Initializing the logger
logger = logging.getLogger(__name__)

# Initializing storage (creating a sample of MemoryStorage class)
storage = MemoryStorage()


# Func of initiation and starting the bot
async def main() -> None:
    # Configure logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # print info about starting the bot
    logger.info('Starting bot')

    # Load configuration into variable config
    config: Config = load_config()

    # Initialize the bot and dispatcher
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # Configure the Menu button
    await set_main_menu(bot)

    # Registry routers in dispatcher
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Scip accumulated updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
