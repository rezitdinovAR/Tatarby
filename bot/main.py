import telebot
from telebot import types

bot = telebot.TeleBot('6388069124:AAHiZIx5t9YEMfr0TTDr37wkBVuyCSJ7olY')

ru = "ru"
tat = "tat"

liked = "liked"
advice = "advice"
top = "top"
search = "search"

languages_keyboard_text = {ru: 'Русский язык', tat: 'Татарча'}

menu_text = {
    "options": {
        ru: "Что вас интересует?",
        tat: "1"
    },
    "language_change": {
        ru: "Ваш язык  изменён на русский",
        tat: "1"
    }
}

options_text = {
    liked: {
        ru: "Список избранно",
        tat: "1"
    },
    advice: {
        ru: "Посоветовать книгу",
        tat: "1"
    },
    top: {
        ru: "Популярные",
        tat: "1"
    },
    search: {
        ru: "Поиск",
        tat: "1"
    }
}

users = {}


def get_user(user_id):
    if user_id in users:
        return users[user_id]
    else:
        return {"language": ru}


def save_user(user_id, user):
    users[user_id] = user


def get_language(user_id):
    return get_user(user_id)["language"]


def change_language_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=languages_keyboard_text[tat], callback_data=tat)
    btn2 = types.InlineKeyboardButton(text=languages_keyboard_text[ru], callback_data=ru)
    markup.add(btn1, btn2)

    return markup


def options_key_board(lang):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text=options_text[liked][lang], callback_data=liked)
    btn2 = types.InlineKeyboardButton(text=options_text[advice][lang], callback_data=advice)
    btn3 = types.InlineKeyboardButton(text=options_text[top][lang], callback_data=top)
    btn4 = types.InlineKeyboardButton(text=options_text[search][lang], callback_data=search)
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)

    return markup



def change_language(message):
    bot.send_message(message.from_user.id, "Выберите язык\n\nТелне сайлагыз", reply_markup=change_language_keyboard())


def ask_options(user_id, language):
    bot.send_message(user_id, menu_text["options"][language], reply_markup=options_key_board(language))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Здравствуйте и Исәнмесез\n\nДля того что бы изменить язык нажмите /settings\n\nТелне үзгәртү өчен, /settings басыгыз")
    language = get_language(message.from_user.id)
    ask_options(message.from_user.id, language)


@bot.message_handler(commands=['settings'])
def settings(message):
    change_language(message)


@bot.callback_query_handler(func=lambda call: call.data in [liked, advice, top, search])
def callback1(call):
    if call.data == liked:
        bot.send_message(call.message.chat.id, "Избранные")
    elif call.data == advice:
        bot.send_message(call.message.chat.id, "Посоветовать")
    elif call.data == top:
        bot.send_message(call.message.chat.id, "Лучшие")
    elif call.data == search:
        bot.send_message(call.message.chat.id, "Поиск")
    bot.answer_callback_query(callback_query_id=call.id, text='Ты гнида')


@bot.callback_query_handler(func=lambda call: call.data in [ru, tat])
def callback_language(call):
    user = get_user(call.from_user.id)
    user["language"] = call.data

    save_user(call.from_user.id, user)

    bot.answer_callback_query(callback_query_id=call.id, text=menu_text["language_change"][call.data])

    ask_options(call.from_user.id, call.data)



@bot.message_handler(content_types=['text'])
def start_handler(message):
    pass
    # if message.text == languages_keyboard_text[ru]:
    #     users[message.from_user.id]["language"] = ru
    #     ask_what_option_user_wants(message.from_user.id, ru)
    # elif message.text == languages_keyboard_text[tat]:
    #     users[message.from_user.id]["language"] = tat
    #     ask_what_option_user_wants(message.from_user.id, tat)
    # else:
    #     if message.from_user.id not in users:
    #         reg_new_user(message)
    #     elif "language" in users[message.from_user.id]:
    #         reg_new_user(message)
    #     else:
    #         language = users[message.from_user.id]["language"]
    #
    #         if message.text == options_keyboard_text[language][music]:
    #             pass
    #         if message.text == options_keyboard_text[language][talk]:
    #             pass
    #         if message.text == options_keyboard_text[language][other]:
    #             pass


if __name__ == '__main__':
    print("started")
    bot.polling(none_stop=True, interval=0)
