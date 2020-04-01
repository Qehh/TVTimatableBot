'''
Поулчаем программу телепередач для определенного канала на сегодня
'''


import requests
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import types
import re

url_1_channel = 'https://tv.akado.ru/channels/1kanal/'
url_matchtv_channel = 'https://tv.akado.ru/channels/matchtv/'
url_2x2_channel = 'https://tv.akado.ru/channels/2x2/'
url_ntv_channel = 'https://tv.akado.ru/channels/ntv/'
url_5_channel = 'https://tv.akado.ru/channels/5kanal/'
url_kultura_channel = 'https://tv.akado.ru/channels/rossiya-k/'
url_russia_24_channel = 'https://tv.akado.ru/channels/rossiya24/'
url_otr_channel = 'https://tv.akado.ru/channels/otr/'
url_tvc_channel = 'https://tv.akado.ru/channels/tvc/'
url_rentv_channel = 'https://tv.akado.ru/channels/rentv/'
url_domashnij_channel = 'https://tv.akado.ru/channels/sts/'
url_tv3_channel = 'https://tv.akado.ru/channels/tv-3/'
url_pyatnica_channel = 'https://tv.akado.ru/channels/pyatnitsa-/'
url_zvezda_channel = 'https://tv.akado.ru/channels/zvezda/'
url_tnt_channel = 'https://tv.akado.ru/channels/tnt/'
url_che_channel = 'https://tv.akado.ru/channels/che/'
url_super_channel = 'https://tv.akado.ru/channels/super/'
url_tv1000_channel = 'https://tv.akado.ru/channels/tv1000russkoekino/'
url_kinotv_channel = 'https://tv.akado.ru/channels/kinotv/'



def get_tv_tmtbl(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser") # создаем объект BeautifulSoup
    s_result = [] # сюда будем записывать каждую передачу как один элемент списка
    for tag in soup.find_all("span"): 
        s = tag.text # получаем передачу по тегу li
        s_result.append(s) # создаем список
        
    s_result = s_result[29:]  # информативная часть страницы начинается отсюда   
    del s_result[2::3] # удаляем каждый третий элемент списка, начиная со второго
    
    template = r'\d\d:\d\d' # для поиска строки, которая не является временем
    
    # удаляем все элементы, которые не являются временем и передачами
    count = 0
    for i in s_result:
        match = re.search(template, i)
        if (count % 2 == 0) and (match == None):
            del s_result[count:]
        count += 1
    
    # соединяем время и название телепередачи в один элемент списка
    count = 0    
    s_result_timetable = []
    for i in range(0, len(s_result), 2):
        programm = s_result[i] + ' ' + s_result[count+1]
        s_result_timetable.append(programm)
        count += 2
    
    
    s_result_timetable.insert(0, soup.title.string[:-42]) # вставляем в итоговый список название телеканала.
                                                          # Имя заголовка страницы
    s_result_timetable.insert(0, datetime.datetime.now().strftime("%d-%m-%Y")) # вставляем дату и время                                                     
    s_result_timetable = '\n'.join(s_result_timetable) # превращаем список в строку    
        
    return s_result_timetable

#print(get_tv_tmtbl(url_1_channel))

###---------------------------------------
bot = telebot.TeleBot('956916797:AAETCR1iz_xmzy9mAZ2ledU5ZTDTVpV38sU')
# Метод, который получает сообщения и обрабатывает их
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Если написали «Привет»
    #if message.text == "Привет":
        # Пишем приветствие
        bot.send_message(message.from_user.id, "Привет, здесь будет ТВ программа на сегодня")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого канала
        key_1_channel = types.InlineKeyboardButton(text='1 канал', callback_data='1_channel')
        # И добавляем кнопку на экран
        keyboard.add(key_1_channel)
        
        #key_5_channel = types.InlineKeyboardButton(text='5 канал', callback_data='5_channel')
        #keyboard.add(key_5_channel)
        
        key_matchtv_channel = types.InlineKeyboardButton(text='МАТЧ ТВ!', callback_data='matchtv_channel')
        keyboard.add(key_matchtv_channel)
        
        
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выберите канал:', reply_markup=keyboard)
    
    #elif message.text == "/help":
    #    bot.send_message(message.from_user.id, "Напиши Привет")
    #else:
    #    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):
    # Если нажали на одну из кнопок — выводим телепрограмму
    if call.data == '1_channel': 
        bot.send_message(call.message.chat.id, get_tv_tmtbl(url_1_channel))
    #if call.data == '5_channel': 
    #    bot.send_message(call.message.chat.id, get_tv_tmtbl(url_5_channel))
    if call.data == 'matchtv_channel': 
        bot.send_message(call.message.chat.id, get_tv_tmtbl(url_matchtv_channel))

# Запускаем постоянный опрос бота в Телеграме

bot.polling(none_stop=True, interval=0)
