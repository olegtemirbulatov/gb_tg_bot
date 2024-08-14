import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import BotCommand, BotCommandScopeDefault

import config



# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = config.token

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функция для настройки меню бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/info", description="Информация о боте"),
        BotCommand(command="/user", description="Информация о пользователе")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logging.info(f"User {message.from_user.id} started the bot")
    await message.answer("Привет! Я простой бот. Используй /info для информации о боте или /user для информации о себе.")


# Обработчик команды /info
@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    logging.info(f"User {message.from_user.id} requested bot info")
    await message.answer("Я простой Telegram бот, созданный с помощью aiogram. У меня есть команды /info и /user.")


# Обработчик команды /user
@dp.message(Command("user"))
async def cmd_user(message: types.Message):
    logging.info(f"User {message.from_user.id} requested user info")
    user = message.from_user
    user_info = f"Информация о пользователе:\n"
    user_info += f"ID: {user.id}\n"
    user_info += f"Имя: {user.first_name}\n"
    user_info += f"Фамилия: {user.last_name}\n" if user.last_name else ""
    user_info += f"Username: @{user.username}\n" if user.username else ""
    await message.answer(user_info)


# Обработчик для всех остальных сообщений
@dp.message()
async def echo(message: types.Message):
    logging.info(f"User {message.from_user.id} sent message: {message.text}")
    await message.answer("Извините, я не понимаю эту команду. Пожалуйста, используйте команды из меню.")


# Функция для запуска бота
async def main():
    # Настройка логирования
    logging.info("Starting bot")
    
    # Установка команд бота
    await set_commands(bot)
    
    # Запуск поллинга
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())