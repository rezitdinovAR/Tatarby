import telebot
from telebot import types

import Translate
from bot.book import Book

import psycopg2

# import stable_dif
import poisk



# stable_dif.init()

bot = telebot.TeleBot('6388069124:AAHiZIx5t9YEMfr0TTDr37wkBVuyCSJ7olY')

ru = "ru"
tat = "tat"

liked = "liked"
advice = "advice"
top = "top"
search = "search"
back = "back"

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
        ru: "Начатые книги",
        tat: "Башылган китаплар"
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
    },
    back: {
        ru: "Назад",
        tat: "Артка"
    }
}

extra = {
    "no_page": {
        ru: "Страницы нет",
        tat: "Битләр юк"
    }
}

books = {}


def init_books():
    conn = psycopg2.connect(dbname='Books', user='user', password='password', host='158.160.19.67', port="5438")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    for i in cursor.fetchall():
        book_id, title_ru, title_tat, desc_ru, desc_tat, url, cover_url, vector = i
        print(book_id)

        with open(f"books/{url.split('/')[-1]}", 'r', encoding="utf-8") as file:
            books[book_id] = Book(int(book_id), title_ru, title_tat, desc_ru, desc_tat, url.split('/')[-1],
                                  "".join(file.readlines()))


users = {}

init_books()


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

def options_key_board_back(lang):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text=options_text[back][lang], callback_data=back)
    markup.add(btn1)

    return markup


controls_keyboard_text = {
    "next": {
        ru: "Далее▶️",
        tat: "Алга▶️"
    },
    "prev": {
        ru: "◀️Назад",
        tat: "◀️Артка"
    },
    "ilus": {
        ru: "Оживить страницу",
        tat: "Рәсем ясарга"
    }
}


def book_controls(book_id, page, language):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=controls_keyboard_text["next"][language], callback_data=f"controls:next:{book_id}:{page}")
    btn2 = types.InlineKeyboardButton(text=controls_keyboard_text["prev"][language], callback_data=f"controls:prev:{book_id}:{page}")
    btn3 = types.InlineKeyboardButton(text=languages_keyboard_text[tat], callback_data=f"controls:tat:{book_id}:{page}")
    btn4 = types.InlineKeyboardButton(text=languages_keyboard_text[ru], callback_data=f"controls:ru:{book_id}:{page}")
    btn5 = types.InlineKeyboardButton(text=controls_keyboard_text["ilus"][language], callback_data=f"controls:ilus:{book_id}:{page}")
    markup.add(btn2, btn1)
    if language == ru:
        markup.add(btn3)
    else:
        markup.add(btn4)
    # markup.add(btn5)

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


@bot.message_handler(func=lambda message: message.text.startswith("/book"))
def open_book(message):
    book_id = int(message.text[5:])
    language = get_language(message.from_user.id)
    page = 0
    user = get_user(message.from_user.id)
    if "cached_books" in user:
        if book_id in user["cached_books"]:
            page = user["cached_books"][book_id]
        else:
            user["cached_books"][book_id] = 0
    else:
        user["cached_books"] = {book_id: 0}
    save_user(message.from_user.id, user)

    text = books[book_id].pages[language][page]


    with open(books[book_id].pages["audio"][page], "rb") as file:
        bot.send_audio(message.from_user.id, audio=file, caption=text, reply_markup=book_controls(book_id, page, language))


@bot.callback_query_handler(func=lambda call: call.data in [liked, advice, top, search, back])
def callback1(call):
    language = get_language(call.from_user.id)
    cid = call.message.chat.id
    mid = call.message.message_id
    if call.data == back:
        bot.edit_message_text(chat_id=cid, message_id=mid, text=menu_text["options"][language], reply_markup=options_key_board(language))
    elif call.data == liked:
        if "cached_books" in get_user(call.from_user.id):
            liked_books = [books[i] for i in get_user(call.from_user.id)["cached_books"].keys()]
            bot.edit_message_text(chat_id=cid, message_id=mid, text="\n\n\n".join([i.to_string(language) for i in liked_books]), reply_markup=options_key_board_back(language))
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Вы пока не начали читать книги')
            return

    elif call.data == advice:
        bot.edit_message_text(chat_id=cid, message_id=mid, text="\n\n\n".join([i.to_string(language) for i in list(set(books.values()))]), reply_markup=options_key_board_back(language))
    elif call.data == top:
        bot.edit_message_text(chat_id=cid, message_id=mid, text="\n\n\n".join([i.to_string(language) for i in books.values()]), reply_markup=options_key_board_back(language))
    elif call.data == search:
        if language == tat:
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Табарга теләгән китапның исемен языгыз", reply_markup=options_key_board_back(language))
        else:
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Напишите название книги, которую хотите найти", reply_markup=options_key_board_back(language))

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
    cont, command, book_id, page = call.data.split(":")
    book_id = int(book_id)
    book = books[book_id]
    page = int(page)




    cid = call.message.chat.id
    mid = call.message.message_id

    if command == "ilus":

        return

    if command == tat or command == ru:
        user = get_user(call.from_user.id)
        user["language"] = command

        save_user(call.from_user.id, user)

    language = get_language(call.from_user.id)
    if command == "prev":
        if page == 0:
            bot.answer_callback_query(callback_query_id=call.id, text=extra["no_page"][language], show_alert=True)
            return
        page -= 1
    elif command == "next":
        if page == len(book.pages[language]) - 1:
            bot.answer_callback_query(callback_query_id=call.id, text=extra["no_page"][language], show_alert=True)
            return
        page += 1


    text = book.pages[language][page]

    user = get_user(call.from_user.id)
    if "cached_books" in user:
        user["cached_books"][book_id] = page
    else:
        user["cached_books"] = {book_id: 0}
    save_user(call.from_user.id, user)
    if command == "next" or command == "prev":
        with open(book.pages["audio"][page], "rb") as file:
            bot.edit_message_media(chat_id=cid, message_id=mid, media=types.InputMediaAudio(file))
    bot.edit_message_caption(chat_id=cid, message_id=mid, caption=text,
                             reply_markup=book_controls(book_id, page, language))

    bot.answer_callback_query(callback_query_id=call.id, text="...")


@bot.message_handler(content_types=['text'])
def start_handler(message):
    language = get_language(message.from_user.id)

    a = poisk.poisk(message.text, books)
    bot.send_message(message.from_user.id, text="\n\n\n".join([i.to_string(language) for i in a]), reply_markup=options_key_board_back(language))



if __name__ == '__main__':
    print("started")
    bot.polling(none_stop=True, interval=0)
