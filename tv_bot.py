'''
Поулчаем программу телепередач для определенного канала на сегодня
'''


import requests
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import types

def get_tv_tmtbl(url): 
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser") # создаем объект BeautifulSoup
    print(soup.title.string[:-49]) # Имя заголовка. Оставляем только название канала
    s_result = [] # сюда будем записывать каждую передачу как один элемент списка
    for tag in soup.find_all("li"): 
            s = tag.text # получаем передачу по тегу li
            s_res = ''
            s_res = s[:5] + ' ' + s[5:-1] # Вставляем пробел после времени начала передачи
                                          # и убираем символ \xa0 в конце каждой строки
            s_result.append(s_res)
            
    s_result_str = '\n'.join(s_result) # преобразовываем список в одну строку для использования
                                       # функции в боте (бот выводит строку, но не список)
    return s_result_str
    
s = datetime.datetime.now().date()
print(s)
url_1_channel = 'https://tv.yandex.ru/channel/pervyy-16?date=' + str(s) # текущая дата
url_5_channel = 'https://tv.yandex.ru/channel/pyatyy-kanal-12?date=' + str(s)
url_tnt_channel = 'https://tv.yandex.ru/channel/tnt-33?date=' + str(s)

print(get_tv_tmtbl(url_tnt_channel))


###---------------------------------------
bot = telebot.TeleBot('956916797:AAETCR1iz_xmzy9mAZ2ledU5ZTDTVpV38sU')
# Метод, который получает сообщения и обрабатывает их
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Если написали «Привет»
    if message.text == "Привет":
        # Пишем приветствие
        bot.send_message(message.from_user.id, "Привет, здесь будет ТВ программа на сегодня")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого канала
        key_1_channel = types.InlineKeyboardButton(text='1 канал', callback_data='1_channel')
        # И добавляем кнопку на экран
        keyboard.add(key_1_channel)
        
        key_5_channel = types.InlineKeyboardButton(text='5 канал', callback_data='5_channel')
        # И добавляем кнопку на экран
        keyboard.add(key_5_channel)
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выберите канал:', reply_markup=keyboard)
    
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == '1_channel': 
        bot.send_message(call.message.chat.id, get_tv_tmtbl(url_1_channel))
    if call.data == '5_channel': 
        bot.send_message(call.message.chat.id, get_tv_tmtbl(url_5_channel))

# Запускаем постоянный опрос бота в Телеграме

bot.polling(none_stop=True, interval=0)