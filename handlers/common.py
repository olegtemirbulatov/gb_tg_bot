import logging
from aiogram import Router, types, F
from aiogram.filters.command import Command

from keyboards.keyboards import kb1
from utils.randomfox import fox


# Ограничение количества запросов от одного пользователя за определенный период времени
FLOOD_CONTROL = 5  # количество запросов
FLOOD_CONTROL_TIME = 60  # время в секундах
flood_control = {}

router = Router()


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        if message.from_user.id in flood_control:
            if flood_control[message.from_user.id] >= FLOOD_CONTROL:
                await message.answer("Вы отправили слишком много запросов. Подождите немного.")
                return
            flood_control[message.from_user.id] += 1
        else:
            flood_control[message.from_user.id] = 1
        logging.info(f"User {message.from_user.id} started the bot")
        await message.answer("Привет! Я простой бот. Используй /info для информации о боте или /user для информации о себе.", reply_markup=kb1)
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /start: {e}")


# Обработчик команды /info
@router.message(Command("info"))
@router.message(F.text.lower() == "инфо")
async def cmd_info(message: types.Message):
    try:
        if message.from_user.id in flood_control:
            if flood_control[message.from_user.id] >= FLOOD_CONTROL:
                await message.answer("Вы отправили слишком много запросов. Подождите немного.")
                return
            flood_control[message.from_user.id] += 1
        else:
            flood_control[message.from_user.id] = 1
        logging.info(f"User {message.from_user.id} requested bot info")
        await message.answer("Я простой Telegram бот, созданный с помощью aiogram. У меня есть команды /info и /user.")
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /info: {e}")


# Обработчик команды /user
@router.message(Command("user"))
@router.message(F.text.lower() == "обо мне")
async def cmd_user(message: types.Message):
    try:
        if message.from_user.id in flood_control:
            if flood_control[message.from_user.id] >= FLOOD_CONTROL:
                await message.answer("Вы отправили слишком много запросов. Подождите немного.")
                return
            flood_control[message.from_user.id] += 1
        else:
            flood_control[message.from_user.id] = 1
        logging.info(f"User {message.from_user.id} requested user info")
        user = message.from_user
        user_info = f"Информация о пользователе:\n"
        user_info += f"ID: {user.id}\n"
        user_info += f"Имя: {user.first_name}\n"
        user_info += f"Фамилия: {user.last_name}\n" if user.last_name else ""
        user_info += f"Username: @{user.username}\n" if user.username else ""
        await message.answer(user_info)
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /user: {e}")


@router.message(Command("fox"))
@router.message(F.text.lower() == "покажи лису")
async def cmd_fox(message: types.Message):
    name = message.chat.first_name
    img_fox = fox()
    await message.answer(f'Держи лису, {name}')
    await message.answer_photo(photo=img_fox)


# Обработчик для всех остальных сообщений
@router.message()
async def echo(message: types.Message):
    try:
        if message.from_user.id in flood_control:
            if flood_control[message.from_user.id] >= FLOOD_CONTROL:
                await message.answer("Вы отправили слишком много запросов. Подождите немного.")
                return
            flood_control[message.from_user.id] += 1
        else:
            flood_control[message.from_user.id] = 1
        logging.info(f"User {message.from_user.id} sent message: {message.text}")
        await message.answer("Извините, я не понимаю эту команду. Пожалуйста, используйте команды из меню.")
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
