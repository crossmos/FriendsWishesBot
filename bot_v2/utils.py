import os
import requests
from dotenv import load_dotenv, find_dotenv
from typing import Optional

from telebot import TeleBot, REPLY_MARKUP_TYPES

from constants import WISHES_URL
from text_constants import (
    ABOUT_TEXT, EMPTY_WISHES_TEXT,
    FRIENDS_LIST_TEXT, SUPPORT_TEXT
)
from keyboards import manage_wishes_keyboard


load_dotenv(find_dotenv())


# Создаём бота
bot = TeleBot(token=str(os.getenv('TELEGRAM_TOKEN')))


# Функция отправки сообщения
def send_message(
        message, text: str, keyboard: Optional[REPLY_MARKUP_TYPES] = None,
        bot: TeleBot = bot
):
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard
    )


# Функции для команд главной клавиатуры
def get_wish_list(message):
    response = requests.get(
        WISHES_URL,
        params={
            'owner_id': message.chat.id
        }
    )

    wishes = response.json()
    wish_list = [wish['title'] for wish in wishes]
    wish_list.reverse()

    if wish_list:
        result_message = '\n'.join(
            [f'{index+1}. {item}' for index,
                item in enumerate(wish_list)]
        )
        send_message(message, result_message, manage_wishes_keyboard())
    else:
        send_message(message, EMPTY_WISHES_TEXT)


def get_friends_list(message):
    send_message(message, FRIENDS_LIST_TEXT)


def get_about_info(message):
    send_message(message, ABOUT_TEXT)


def get_help_info(message):
    send_message(message, SUPPORT_TEXT)


# Дополнительные функции
def add_wish(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f'"{message.text.capitalize()}" добавлено в ваш WishList'
    )
    requests.post(
        WISHES_URL,
        json={
            'title': message.text,
            'owner': message.chat.id
        }

    )


def get_wish(wish_id):
    response = requests.get(
        f'{WISHES_URL}{wish_id}/'
    )
    return response.json()


def get_result_wish_data(wish):
    result_data = []
    result_data.append(f"Название: {wish['title']}")
    if wish['description']:
        result_data.append(f"Описание: {wish['description']}")
    if wish['price']:
        result_data.append(f"Цена: {wish['price']}")
    if wish['link']:
        result_data.append(f"Ссылка: {wish['link']}")
    return result_data
