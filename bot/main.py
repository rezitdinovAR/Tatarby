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
        tat: "Cезне нәрсә кызыксындыра?"
    },
    "language_change": {
        ru: "Ваш язык  изменён на русский",
        tat: "Татар теленә үзгәртелде"
    }
}

options_text = {
    liked: {
        ru: "Список избранного",
        tat: "Сайланганнар исемлеге"
    },
    advice: {
        ru: "Посоветовать книгу",
        tat: "Китап киңәшерю"
    },
    top: {
        ru: "Популярные",
        tat: "Танылган"
    },
    search: {
        ru: "Поиск",
        tat: "Эзләү"
    }
}

extra = {
    "no_page": {
        ru: "Страницы нет",
        tat: ""
    }
}

books = {
    1: {
        "title": {
            ru: "",
            tat: ""
        },
        "desc": {
            ru: "",
            tat: ""
        },
        "cover": "",
        "content": ""
    },
    2: {
        "title": {
            ru: "",
            tat: ""
        },
        "desc": {
            ru: "",
            tat: ""
        },
        "cover": "",
        "content": ""
    },
    3: {
        "title": {
            ru: "",
            tat: ""
        },
        "desc": {
            ru: "",
            tat: ""
        },
        "cover": "",
        "content": ""
    }
}

users = {}

with open("books/1984.txt", 'r', encoding="utf-8") as file:
    books[1]["content"] = "".join(file.readlines())


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


def book_controls(book_id, l, r):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="◀️артка", callback_data=f"controls:prev:{book_id}:{l}:{r}")
    btn2 = types.InlineKeyboardButton(text="алга▶️", callback_data=f"controls:next:{book_id}:{l}:{r}")
    markup.add(btn1, btn2)

    return markup


def get_page(book_id, l, r, is_right):
    book = books[book_id]
    new = -1
    if is_right:
        for i in range(r, min(r + 1000, len(book["content"]))):
            if book["content"][i] == " ":
                new = i
        return [book["content"][r: new], book_controls(book_id, r, new)]
    else:
        for i in range(l, max(l - 1000, 0), -1):
            if book["content"][i] == " ":
                new = i
        return [book["content"][new: l], book_controls(book_id, new, l)]


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


@bot.message_handler(func=lambda message: message.text.startswith("/book"))
def open_book(message):
    book_id = int(message.text[5:])
    text_controls = get_page(book_id, 0, 0, True)
    bot.send_message(message.from_user.id, text_controls[0], reply_markup=text_controls[1])


@bot.callback_query_handler(func=lambda call: call.data in [liked, advice, top, search])
def callback1(call):
    if call.data == liked:
        bot.send_message(call.message.chat.id, "1984\n\n/book1")
    elif call.data == advice:
        bot.send_message(call.message.chat.id, "1984\n\n/book1")
    elif call.data == top:
        bot.send_message(call.message.chat.id, "1984\n\n/book1")
    elif call.data == search:
        bot.send_message(call.message.chat.id, "1984\n\n/book1")
    bot.answer_callback_query(callback_query_id=call.id, text='<3')


@bot.callback_query_handler(func=lambda call: call.data in [ru, tat])
def callback_language(call):
    user = get_user(call.from_user.id)
    user["language"] = call.data

    save_user(call.from_user.id, user)

    bot.answer_callback_query(callback_query_id=call.id, text=menu_text["language_change"][call.data])

    ask_options(call.from_user.id, call.data)


@bot.callback_query_handler(func=lambda call: call.data.startswith("controls"))
def flip_pages(call):
    cont, side, book_id, l, r = call.data.split(":")
    book_id = int(book_id)
    l = int(l)
    r = int(r)

    cid = call.message.chat.id
    mid = call.message.message_id

    text_controls = get_page(book_id, l, r, side == "next")
    if len(text_controls[0]) == 0:
        bot.answer_callback_query(callback_query_id=call.id, text=extra["no_page"][ru])
        return

    bot.edit_message_text(chat_id=cid, message_id=mid, text=text_controls[0], reply_markup=text_controls[1])
    bot.answer_callback_query(callback_query_id=call.id, text="...")


# @bot.message_handler(content_types=['text'])
# def start_handler(message):
#     with open("audio.ogg", "rb") as file:
#         bot.send_audio(message.from_user.id, audio=file, caption="Шамиль", reply_markup=book_controls(1, 0, 1000))


if __name__ == '__main__':
    print("started")
    bot.polling(none_stop=True, interval=0)
