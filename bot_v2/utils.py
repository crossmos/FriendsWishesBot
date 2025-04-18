import os
import requests
from dotenv import load_dotenv, find_dotenv
from typing import Optional

from telebot import TeleBot, REPLY_MARKUP_TYPES
from telebot.types import InlineKeyboardMarkup

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
    msg = bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard
    )
    return msg


# Функция изменения сообщения
def edit_message(
    callback, text: str, keyboard: Optional[InlineKeyboardMarkup] = None,
    bot: TeleBot = bot
):
    bot.edit_message_text(
        text=text,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=keyboard
    )


# Функция изменения клавиатуры
def edit_keyboard(
    callback, keyboard: Optional[InlineKeyboardMarkup] = None,
    bot: TeleBot = bot
):
    bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=keyboard
    )


# Функция удаления сообщения
def delete_message(callback):
    bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )


# Функции для команд главной клавиатуры
def get_owner_wishes_text(message) -> str:
    wishes = get_wishes(message)
    wish_list = []
    counter = 1

    if wishes:
        for wish in wishes:
            wish_list.append(f"{counter}. {wish['title']}")
            if wish['price']:
                wish_list.append(f"Цена: {wish['price']}")
            counter += 1
        text = '\n'.join(wish_list)
        return text
    return EMPTY_WISHES_TEXT


def get_friend_wishes_text(message):
    wishes = get_wishes(message, is_owner=False)
    counter = 1
    if wishes:
        text = ''
        for wish in wishes:
            wish = [
                item for item in get_wish_data(wish)
            ]
            text += (str(counter) + '. ' + '\n'.join(wish) + '\n'
                     + '------------------------------------' + '\n')
            counter += 1
        return text
    return f'У {message.text[1:]}, ещё нет желаний'


def get_friend_text(message) -> str:
    return FRIENDS_LIST_TEXT


def get_about_text(message) -> str:
    return ABOUT_TEXT


def get_help_text(message) -> str:
    return SUPPORT_TEXT


# Функции для взаимодействия с желанием
def add_wish(message):
    requests.post(
        WISHES_URL,
        json={
            'title': message.text,
            'owner': message.chat.id
        }

    )


def edit_wish(message, wish_id, update_parametr):
    requests.patch(
        f'{WISHES_URL}{wish_id}/',
        json={
            update_parametr: message.text
        }
    )


def delete_wish(wish_id):
    requests.delete(
        f'{WISHES_URL}{wish_id}/'
    )


def get_wish(wish_id):
    response = requests.get(
        f'{WISHES_URL}{wish_id}/'
    )
    return response.json()


def get_wish_id(callback):
    wish_id = ''.join(
        [letter for letter in callback.data if letter.isdigit()]
    )
    return wish_id


def get_wishes(message, is_owner: bool = True):
    if is_owner:
        response = requests.get(
            WISHES_URL,
            params={
                'owner_id': message.chat.id
            }
        )
    else:
        response = requests.get(
            WISHES_URL,
            params={
                'owner_username': message.text[1:]
            }
        )
    wishes = response.json()
    return wishes


def get_wishes_ids(callback):
    wishes = get_wishes(callback.message)
    wishes_ids = [wish['id'] for wish in wishes]
    wishes_ids.reverse()
    return wishes_ids


def get_wish_data(wish):
    data = []
    data.append(f"{wish['title']}")
    if wish['description']:
        data.append(f"Описание: {wish['description']}")
    if wish['price']:
        data.append(f"Цена: {wish['price']}")
    if wish['link']:
        data.append(f"Ссылка: {wish['link']}")
    return data


def update_parametr(callback, wish, wish_id, parametr: str):
    if callback.data.startswith(f'update_{parametr}'):
        msg = send_message(
            callback.message,
            text='Введите новое значение'
        )

        def update(msg):
            edit_wish(msg, wish_id=wish_id, update_parametr=parametr)
            text = get_owner_wishes_text(msg)
            send_message(msg, text=text, keyboard=manage_wishes_keyboard())

        bot.register_next_step_handler(
            msg,
            update
        )
