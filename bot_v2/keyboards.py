from telebot import types

from text_constants import (
    GET_MY_WISH_LIST_TEXT,
    GET_FRIEND_WISH_LIST_TEXT,
    GET_ABOUT_INFO_TEXT,
    GET_HELP_INFO_TEXT,
)


# Основная клавиатура
def main_keyboard():
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_keyboard.row(
        types.KeyboardButton(GET_MY_WISH_LIST_TEXT),
        types.KeyboardButton(GET_FRIEND_WISH_LIST_TEXT)
    )
    main_keyboard.row(
        types.KeyboardButton(GET_ABOUT_INFO_TEXT),
        types.KeyboardButton(GET_HELP_INFO_TEXT),

    )
    return main_keyboard


# Клавиатура выбора действия с желанием
def manage_wishes_keyboard():
    manage_wishes_keyboard = types.InlineKeyboardMarkup()
    manage_wishes_keyboard.add(
        types.InlineKeyboardButton(
            'Редактировать',
            callback_data='update')
    )
    manage_wishes_keyboard.add(
        types.InlineKeyboardButton(
            'Удалить',
            callback_data='delete'),
    )
    return manage_wishes_keyboard


# Клавиатура выбора желания для действия
def wish_list_keyboard(callback, wish_list):
    wish_list_keyboard = types.InlineKeyboardMarkup(row_width=5)
    # Тут надо как то отформотировать вид кнопок
    # Чтобы было по 5 в ряду + "Отмена" в конце
    for i in range(len(wish_list)):
        wish_list_keyboard.add(types.InlineKeyboardButton(
            i + 1, callback_data=callback.data + str(wish_list[i])))

    wish_list_keyboard.add(
        types.InlineKeyboardButton(
            'Отменить',
            callback_data='back'
        )
    )
    return wish_list_keyboard


# Клавиатура подтверждения удаления
def confirm_delete_keyboard(wish_id):
    confirm_delete_keyboard = types.InlineKeyboardMarkup()
    confirm_delete_keyboard.add(types.InlineKeyboardButton(
        'Подтвердить удаление',
        callback_data='delete_confirm' + str(wish_id)
    ))
    confirm_delete_keyboard.add(types.InlineKeyboardButton(
        'Отмена', callback_data='confirm_back'))
    return confirm_delete_keyboard


def update_parametrs_list_keyboard(wish_id):
    update_parametrs_list_keyboard = types.InlineKeyboardMarkup(
        row_width=2)
    update_parametrs_list_keyboard.row(
        types.InlineKeyboardButton(
            'Название',
            callback_data='update_title' + str(wish_id)
        ),
        types.InlineKeyboardButton(
            'Описание',
            callback_data='update_description' + str(wish_id)
        )
    )
    update_parametrs_list_keyboard.row(
        types.InlineKeyboardButton(
            'Цена',
            callback_data='update_price' + str(wish_id)
        ),
        types.InlineKeyboardButton(
            'Ссылка',
            callback_data='update_link' + str(wish_id)
        )
    )
    update_parametrs_list_keyboard.add(
        types.InlineKeyboardButton(
            'Отменить',
            callback_data='confirm_back'
        )
    )
    return update_parametrs_list_keyboard


def confirm_update_keyboard(wish_id):
    confirm_update_keyboard = types.InlineKeyboardMarkup()
    confirm_update_keyboard.add(types.InlineKeyboardButton(
        'Подтвердить редактирование',
        callback_data='confirm_delete' + str(wish_id)
    ))
    confirm_update_keyboard.add(types.InlineKeyboardButton(
        'Отмена', callback_data='confirm_back'))
    return confirm_update_keyboard
