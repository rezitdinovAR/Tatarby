import telebot
from telebot import types

bot = telebot.TeleBot('6388069124:AAHiZIx5t9YEMfr0TTDr37wkBVuyCSJ7olY')

ru = "ru"
tat = "tat"

music = "music"
talk = "talk"
other = "other"


languages_keyboard_text = {ru: 'Русский язык', tat: 'Татарча'}
options_text = {ru: "Чё хочешь?", tat: "Чё хочешь [на татарском]?"}
options_keyboard_text = {
    ru: {
        music: "Музыку",
        talk: "Поговорить",
        other: "Другое",

    },
    tat: {
        music: "Музыку",
        talk: "Поговорить",
        other: "Другое"
    }

}
users = {}


def change_language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text=languages_keyboard_text[tat])
    btn2 = types.KeyboardButton(text=languages_keyboard_text[ru])
    markup.add(btn1, btn2)

    return markup



def options_key_board(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton(text=options_keyboard_text[lang][music])
    btn2 = types.KeyboardButton(text=options_keyboard_text[lang][talk])
    btn3 = types.KeyboardButton(text=options_keyboard_text[lang][other])
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    return markup


def ask_what_option_user_wants(user_id, lang):
    bot.send_message(user_id, options_text[lang], reply_markup=options_key_board(lang))


# def reg_new_user(message):
#     users[message.from_user.id] = {}
#     bot.send_message(message.from_user.id, "Здравствуйте и Исәнмесез", reply_markup=change_language_keyboard())


def change_language(message):
    bot.send_message(message.from_user.id, "Выберите язык\n\nТелне сайлагыз", reply_markup=change_language_keyboard())


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Здравствуйте и Исәнмесез")


@bot.message_handler(commands=['settings'])
def settings(message):
    change_language(message)


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




bot.polling(none_stop=True, interval=0)
