import asyncio
import logging

from aiogram import Dispatcher, Bot

from config_data.config import load_config, Config
from handlers import user_handlers


# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
            level=logging.INFO,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
            u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим информацию о старте бота
    logger.info('Starting Bot')

    # Инициализируем config
    config: Config = load_config()

    bot: Bot = Bot(token=config.bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Регистрация хэндлеров
    dp.include_router(user_handlers.router)

    # Удаление старых апдейтов и запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stoped!')
