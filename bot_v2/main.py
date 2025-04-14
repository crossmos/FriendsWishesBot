import re
import requests

from constants import TELEGRAM_USERS_URL, WISHES_URL
from text_constants import (
    HELLO_TEXT,
    REGISTRY_REPLY_TEXT,
    GET_MY_WISH_LIST_TEXT,
    GET_FRIEND_WISH_LIST_TEXT,
    GET_ABOUT_INFO_TEXT,
    GET_HELP_INFO_TEXT,
)
from keyboards import (
    main_keyboard,
    manage_wishes_keyboard,
    confirm_delete_keyboard,
    update_parametrs_list_keyboard,
    # confirm_update_keyboard,
    wish_list_keyboard,
)
from utils import (
    bot,
    add_wish,
    get_wish,
    get_wish_list,
    get_friends_list,
    get_about_info,
    get_help_info,
    get_result_wish_data,
    send_message,
)


MAIN_KEYBOARD_COMMANDS = {
    GET_MY_WISH_LIST_TEXT: get_wish_list,
    GET_FRIEND_WISH_LIST_TEXT: get_friends_list,
    GET_ABOUT_INFO_TEXT: get_about_info,
    GET_HELP_INFO_TEXT: get_help_info
}


# Обработка начала работы бота
@bot.message_handler(commands=['start'])
def start_bot(message):
    try:
        response = requests.get(
            f'{TELEGRAM_USERS_URL}{message.chat.id}/'
        )
        if response.status_code == 200:
            send_message(message, REGISTRY_REPLY_TEXT)
        else:
            response = requests.post(
                TELEGRAM_USERS_URL,
                json={
                    'username': message.chat.username,
                    'telegram_id': message.chat.id
                }
            )
            send_message(message, HELLO_TEXT, main_keyboard())

    except requests.exceptions.RequestException as error:
        print(f'Ошибка: {error}')


# Обработка текстовых сообщений от пользователя
@bot.message_handler(content_types=['text'])
def bot_management(message):
    if message.text in MAIN_KEYBOARD_COMMANDS:
        MAIN_KEYBOARD_COMMANDS[message.text](message)

    elif message.text.startswith('@'):
        response = requests.get(
            WISHES_URL,
            params={
                'owner_username': message.text[1:]
            }
        )
        wishes = response.json()

        if len(wishes) == 0:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'У {message.text[1:]}, ещё нет желаний'
            )
        else:
            result_message = ''
            for wish in wishes:
                wish = [
                    item for item in get_result_wish_data(wish)
                ]
                result_message = '\n'.join(wish)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=result_message
                )
    else:
        add_wish(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'back')
def back_button_handker(callback):
    bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=manage_wishes_keyboard()
    )


# @bot.callback_query_handler(
#     func=lambda callback: callback.data == 'confirm_back'
# )
# def confirm_back_button_handler(callback):
#     bot.edit_message_text(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#         text=get_wish_list(callback.message),
#         reply_markup=manage_wishes_keyboard()
#     )


@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def delete_wish_list_handler(callback):
    response = requests.get(
        WISHES_URL,
        params={
            'owner_id': callback.message.chat.id
        }
    )
    wishes = response.json()
    wish_list_ids = [wish['id'] for wish in wishes]
    wish_list_ids.reverse()

    bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=wish_list_keyboard(callback, wish_list_ids)
    )


@bot.callback_query_handler(
    func=lambda callback: re.search(r'^delete\d+$', callback.data)
)
def confirm_delete_wish_handler(callback):
    wish_id = ''.join(
        [letter for letter in callback.data if letter.isdigit()]
    )

    result_message = '\n'.join(
        [item for item in get_result_wish_data(get_wish(wish_id))]
    )

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=result_message,
        reply_markup=confirm_delete_keyboard(wish_id)
    )


# @bot.callback_query_handler(
#     func=lambda callback: re.search(r'^delete_confirm\d+$', callback.data)
# )
# def delete_wish_handler(callback):
#     wish_id = ''.join(
#         [letter for letter in callback.data if letter.isdigit()]
#     )
#     requests.delete(
#         f'{WISHES_URL}{wish_id}/'
#     )
#     bot.edit_message_text(
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#         text=get_wish_list(callback.message),
#         reply_markup=manage_wishes_keyboard()
#     )


@bot.callback_query_handler(func=lambda callback: callback.data == 'update')
def update_wish_list_handler(callback):
    response = requests.get(
        WISHES_URL,
        params={
            'owner_id': callback.message.chat.id
        }
    )
    wishes = response.json()
    wish_list_ids = [wish['id'] for wish in wishes]
    wish_list_ids.reverse()

    bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=wish_list_keyboard(callback, wish_list_ids)
    )


@bot.callback_query_handler(
    func=lambda callback: re.search(r'^update\d+$', callback.data)
)
def choose_parametr_update_handler(callback):
    wish_id = ''.join(
        [letter for letter in callback.data if letter.isdigit()]
    )
    result_message = '\n'.join(
        [item for item in get_result_wish_data(get_wish(wish_id))])

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=result_message,
        reply_markup=update_parametrs_list_keyboard(wish_id)
    )


@bot.callback_query_handler(
    func=lambda callback: re.search(r'update\w{5,12}\d+$', callback.data)
)
def confirm_update_wish_handler(callback):
    wish_id = ''.join(
        [letter for letter in callback.data if letter.isdigit()]
    )

    if callback.data.startswith('update_title'):
        msg = bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"Введите новое название для {get_wish(wish_id)['title']}"
        )
        bot.register_next_step_handler(
            msg,
            edit_wish,
            wish_id=wish_id,
            update_parametr='title'
        )


def edit_wish(message, wish_id, update_parametr):
    requests.patch(
        f'{WISHES_URL}{wish_id}/',
        json={
            update_parametr: message.text
        }
    )


bot.polling()
