import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

import config
from handlers import common, career_choice



# Функция для настройки меню бота
async def set_commands(bot: Bot):
    try:
        commands = [
            BotCommand(command="/start", description="Начать работу с ботом"),
            BotCommand(command="/info", description="Информация о боте"),
            BotCommand(command="/user", description="Информация о пользователе")
        ]
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    except Exception as e:
        logging.error(f"Ошибка при настройке меню бота: {e}")


# Функция для запуска бота
async def main():
    try:
        # Настройка логирования
        logging.basicConfig(level=logging.INFO)

        # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
        API_TOKEN = config.token

        # Инициализация бота и диспетчера
        bot = Bot(token=API_TOKEN)
        dp = Dispatcher()

        dp.include_router(career_choice.router)
        dp.include_router(common.router)

        # Настройка логирования
        logging.info("Starting bot")
        
        # Установка команд бота
        await set_commands(bot)
        
        # Запуск поллинга
        await dp.start_polling(bot)
    
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())
