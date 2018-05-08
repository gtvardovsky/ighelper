import telebot
import requests
import io
from opengraph import OpenGraph
from telebot import types
import botan
TOKEN = '516292907:AAFBu0-NJvhs0xTbGtIkHEAzhpZIe6uQNSk'
bot = telebot.TeleBot(TOKEN)
global check
check = ''
myChatId = '264106145'
botan_key = '9e6aba31-0d68-4d71-8734-acacca48f792'


@bot.message_handler(commands=['start'])
def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.row('Фото поста','Абзацы')
    keyboard.row('Видео поста','💬')
    bot.send_message(message.chat.id,'С чем тебе помочь?',reply_markup = keyboard)
    botan.track(botan_key, message.chat.id, message, 'Запуск бота')


@bot.message_handler(func=lambda message: check == 'callBack')
def callBack(message):
    if (message.text == 'Фото поста') or (message.text == 'Абзацы') or (message.text == '💬') or (message.text == 'Видео поста'):
        global check
        chek = ''
        Choose_menu(message)
        return
    msg = message.text
    bot.send_message(myChatId,'Пользователь: @{username}\nСообщение: {msg}'.format(username = message.from_user.first_name, msg = msg))
    bot.send_message(message.chat.id,'Спасибо за обратную связь!')
    global check
    check = ''



@bot.message_handler(func=lambda message: check == 'abz')
def Abz(message):
    if (message.text == 'Фото поста') or (message.text == '💬') or (message.text == 'Видео поста') :
        global check
        chek = ''
        Choose_menu(message)
        return
    s = message.text
    s2 = s.splitlines()
    result = ''
    for i in range(len(s2)):
         result = result + str(s2[i]) + '⠀' + '\n'
    bot.send_message(message.chat.id,text = result)
    if len(s) > 2000 :
        bot.send_message(message.chat.id, text = 'Максимальное количество символов, которое разрешает instagram - 2000\nУ тебя вышло - {len}\nПопробуй сократить текст'.format(len = str(len(s))))
    else:
        bot.send_message(message.chat.id,text = 'Просто скопируй текст 👆🏼 и вставь в описание поста 📱')


@bot.message_handler(func=lambda message: check == 'photo')
def Text(message):
    if (message.text == 'Абзацы') or (message.text == '💬') or (message.text == 'Видео поста'):
        global check
        chek = ''
        Choose_menu(message)
        return
    url = message.text + 'media/?size=l'
    if (url.find("www.instagram.com")!= -1) or (url.find ("instagram.com") != -1):
        try:
            response = requests.get(url)
            photo = ('photo.jpg', io.BytesIO(response.content))
            bot.send_photo(message.chat.id,photo)
        except:
            bot.send_message(message.chat.id,' Либо аккаунт закрыт, либо с твоей ссылкой что-то не так\nПроверь ее и пришли заново')
    else :
        bot.send_message(message.chat.id,'Пришли мне ссылку на фото из INSTAGRAM')
        
@bot.message_handler(func=lambda message: check == 'video')
def Video(message):
    if (message.text == 'Абзацы') or (message.text == '💬') or (message.text == 'Фото поста'):
        global check
        chek = ''
        Choose_menu(message)
        return
    url = message.text
    if (url.find("www.instagram.com")!= -1) or (url.find ("instagram.com") != -1):
        video = OpenGraph(url = url)
        try:
            url_video = str(video.video)
            response = requests.get(url_video)
            video = ('video.mp4', io.BytesIO(response.content))
            bot.send_message(message.chat.id,'Секунду, загружаю...')
            bot.send_video(message.chat.id, video)
        except:
            bot.send_message(message.chat.id,' Либо аккаунт закрыт, либо с твоей ссылкой что-то не так\nПроверь ее и пришли заново')
    else :
        bot.send_message(message.chat.id,'Пришли мне ссылку на видео из INSTAGRAM')
    chek = ''


@bot.message_handler(content_types=["text"])
def Choose_menu(message):
    if (message.text == 'Видео поста'):
        bot.send_message(message.chat.id,'Пришли мне ссылку на видео из instagram\nАккаунт должен быть окрытым')
        global check
        check = 'video'
        botan.track(config.botan_key, message.chat.id, message, 'Видео')
    if (message.text == 'Абзацы'):
        bot.send_message(message.chat.id,'Пришли мне текст, разделенный обычными абзацами\n(Я имею в виду, чтобы между абзацами была пустая строка)')
        check = 'abz'
        botan.track(botan_key, message.chat.id, message, 'Абзацы')
    if (message.text == 'Фото поста'):
        bot.send_message(message.chat.id,'Пришли мне ссылку на пост из instagram\nАккаунт должен быть окрытым')
        check = "photo"
        botan.track(botan_key, message.chat.id, message, 'Фото поста')
    if (message.text == '💬'):
        bot.send_message(message.chat.id,'Если ты обнаружил(а) какую-то неисправность, хочешь что-то предложить или задать вопрос - напиши 👇')
        check = "callBack"


bot.polling()
