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
            text='Редактировать',
            callback_data='update')
    )
    manage_wishes_keyboard.add(
        types.InlineKeyboardButton(
            text='Удалить',
            callback_data='delete'),
    )
    return manage_wishes_keyboard


# Клавиатура со списком желаний
def wish_list_keyboard(callback, wishes_ids):
    wish_list_keyboard = types.InlineKeyboardMarkup()
    wishes = []

    for i in range(len(wishes_ids)):
        wishes.append(types.InlineKeyboardButton(
            text=i + 1, callback_data=callback.data + str(wishes_ids[i])
        ))
        if len(wishes) == 5:
            wish_list_keyboard.row(*wishes)
            wishes.clear()

    wish_list_keyboard.row(*wishes)
    wish_list_keyboard.add(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data='back'
        )
    )
    return wish_list_keyboard


# Клавиатура подтверждения удаления
def delete_confirm_keyboard(wish_id):
    delete_confirm_keyboard = types.InlineKeyboardMarkup()
    delete_confirm_keyboard.add(types.InlineKeyboardButton(
        text='Удалить',
        callback_data='delete_confirm' + str(wish_id)
    ))
    delete_confirm_keyboard.add(types.InlineKeyboardButton(
        text='Отменить',
        callback_data='cancel'
    ))
    return delete_confirm_keyboard


# Клавиатура выбора параметра редактирования
def update_parametr_keyboard(wish_id):
    update_parametrs_list_keyboard = types.InlineKeyboardMarkup(
        row_width=2)
    update_parametrs_list_keyboard.row(
        types.InlineKeyboardButton(
            text='Название',
            callback_data='update_title' + str(wish_id)
        ),
        types.InlineKeyboardButton(
            text='Описание',
            callback_data='update_description' + str(wish_id)
        )
    )
    update_parametrs_list_keyboard.row(
        types.InlineKeyboardButton(
            text='Цена',
            callback_data='update_price' + str(wish_id)
        ),
        types.InlineKeyboardButton(
            text='Ссылка',
            callback_data='update_link' + str(wish_id)
        )
    )
    update_parametrs_list_keyboard.add(
        types.InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel'
        )
    )
    return update_parametrs_list_keyboard


def update_confirm_keyboard(wish_id):
    confirm_update_keyboard = types.InlineKeyboardMarkup()
    confirm_update_keyboard.add(types.InlineKeyboardButton(
        text='Подтвердить редактирование',
        callback_data='confirm_delete' + str(wish_id)
    ))
    confirm_update_keyboard.add(types.InlineKeyboardButton(
        text='Отмена',
        callback_data='confirm_back'
    ))
    return confirm_update_keyboard
