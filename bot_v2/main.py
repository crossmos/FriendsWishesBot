import re
import requests

from constants import TELEGRAM_USERS_URL  # WISHES_URL
from text_constants import (
    HELLO_TEXT,
    REGISTRY_REPLY_TEXT,
    GET_MY_WISH_LIST_TEXT,
    GET_FRIEND_WISH_LIST_TEXT,
    GET_ABOUT_INFO_TEXT,
    GET_HELP_INFO_TEXT,
)
from keyboards import (
    delete_confirm_keyboard,
    manage_wishes_keyboard,
    main_keyboard,
    update_parametr_keyboard,
    # update_confirm_keyboard,
    wish_list_keyboard,
)
from utils import (
    add_wish,
    bot,
    # delete_message,
    delete_wish,
    edit_message,
    # edit_wish,
    edit_keyboard,
    get_about_text,
    get_friend_text,
    get_friend_wishes_text,
    get_owner_wishes_text,
    get_help_text,
    get_wish,
    get_wish_id,
    get_wish_data,
    get_wishes_ids,
    send_message,
)


MAIN_KEYBOARD_COMMANDS = {
    GET_MY_WISH_LIST_TEXT: get_owner_wishes_text,
    GET_FRIEND_WISH_LIST_TEXT: get_friend_text,
    GET_ABOUT_INFO_TEXT: get_about_text,
    GET_HELP_INFO_TEXT: get_help_text
}


# Обработка начала работы бота
@bot.message_handler(commands=['start'])
def bot_start(message):
    try:
        response = requests.get(
            f'{TELEGRAM_USERS_URL}{message.chat.id}/'
        )
        if response.status_code == 200:
            send_message(message, REGISTRY_REPLY_TEXT, main_keyboard())
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

    # Обработка команд с основной клавиатуры
    if message.text in MAIN_KEYBOARD_COMMANDS:
        text = MAIN_KEYBOARD_COMMANDS[message.text](message)
        if message.text == GET_MY_WISH_LIST_TEXT:
            send_message(
                message=message, text=text,
                keyboard=manage_wishes_keyboard()
            )
        else:
            send_message(message=message, text=text)

    # Взаимодействие с друзьями
    elif message.text.startswith('@'):
        text = get_friend_wishes_text(message)
        send_message(message=message, text=text)

    # Если текст не команда и не username, то добавляем как желание
    else:
        add_wish(message)
        send_message(
            message, f'"{message.text.capitalize()}" добавлено в ваш WishList'
        )


# Получения списка желаний для удаления/редактирования
@bot.callback_query_handler(
    func=lambda callback: (
        (callback.data == 'delete') or (callback.data == 'update')
    )
)
def get_wish_list_keyboard(callback):
    wishes_ids = get_wishes_ids(callback)
    edit_keyboard(
        callback=callback,
        keyboard=wish_list_keyboard(callback, wishes_ids)
    )


# Функция возврата к списку желаний
@bot.callback_query_handler(func=lambda callback: callback.data == 'back')
def back_button_handler(callback):
    edit_keyboard(
        callback=callback,
        keyboard=manage_wishes_keyboard()
    )


# Функция отмены удаления/редактирования
@bot.callback_query_handler(
    func=lambda callback: callback.data == 'cancel'
)
def cancel_button_handler(callback):
    text = get_owner_wishes_text(callback.message)
    edit_message(
        callback=callback, text=text, keyboard=manage_wishes_keyboard()
    )


# Подтверждение удаления желания
@bot.callback_query_handler(
    func=lambda callback: re.search(r'^delete\d+$', callback.data)
)
def delete_confirm_handler(callback):
    wish_id = get_wish_id(callback=callback)
    wish = get_wish(wish_id)
    result_message = 'Удалить это желание?\n' + '\n'.join(
        [item for item in get_wish_data(wish)]
    )
    edit_message(
        callback=callback,
        text=result_message,
        keyboard=delete_confirm_keyboard(wish_id)
    )


# Удаление желания
@bot.callback_query_handler(
    func=lambda callback: re.search(r'^delete_confirm\d+$', callback.data)
)
def delete_handler(callback):
    wish_id = get_wish_id(callback=callback)
    delete_wish(wish_id)
    text = get_owner_wishes_text(callback.message)
    edit_message(
        callback=callback, text=text, keyboard=manage_wishes_keyboard()
    )


# Выбор параметра для редактирования
@bot.callback_query_handler(
    func=lambda callback: re.search(r'^update\d+$', callback.data)
)
def choose_parametr_update_handler(callback):
    wish_id = get_wish_id(callback=callback)
    wish = get_wish(wish_id)
    text = '\n'.join(
        [item for item in get_wish_data(wish)])
    edit_message(
        callback=callback, text=text,
        keyboard=update_parametr_keyboard(wish_id=wish_id)

    )


# @bot.callback_query_handler(
#     func=lambda callback: re.search(r'update\w{5,12}\d+$', callback.data)
# )
# def confirm_update_wish_handler(callback):
#     wish_id = ''.join(
#         [letter for letter in callback.data if letter.isdigit()]
#     )
#     if callback.data.startswith('update_title'):
#         msg = bot.send_message(
#             chat_id=callback.message.chat.id,
#             text=f"Введите новое название для {get_wish(wish_id)['title']}"
#         )
#         bot.register_next_step_handler(
#             msg,
#             edit_wish,
#             wish_id=wish_id,
#             update_parametr='title'
#         )

bot.polling(timeout=None)
