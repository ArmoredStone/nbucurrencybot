import config
import telebot
from telebot import types
import requests
import json
import time
import datetime

bot = telebot.TeleBot(config.token)
now = datetime.datetime.now()

def date_generator(now):
    final_str = ''
    final_str += str(now.year)
    if now.month<10:
        final_str= final_str+'0'+str(now.month)+str(now.day)
    else:
        final_str+=str(now.month)+str(now.day)
    return final_str

def finding_needed_dictionary(array_of_dictionaries,r030_code):
    for k in array_of_dictionaries:
        print(k)
        if(k.get('r030') == r030_code):
            return k


@bot.message_handler(commands=['start','help'])
def start(message):
    bot.send_message(message.chat.id,"Здравствуйте, я неоффициальный бот работающий с помощью API сайта НБУ. Список моих команд: \n/course\n/help")
@bot.message_handler(commands=['course'])
def handle_course(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('RUB','USD','EUR')
    a = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date='+date_generator(now)+'&json')
    x = json.loads(a.text)
    bot.send_message(message.chat.id,"Для какой валюты вы хотите узнать текущий курс? Чтобы убрать контекстное меню отправьте любое сообщение.", reply_markup=markup)
    @bot.message_handler(content_types='text')
    def different_currencies(message):
        if(message.text=="RUB"):
            dictionary = finding_needed_dictionary(x, 643)
            bot.send_message(message.chat.id,"Текущий курс рубля по отношению к гривне: "+str(round(dictionary.get('rate'),2)))
        elif(message.text=="USD"):
            dictionary = finding_needed_dictionary(x, 840)
            bot.send_message(message.chat.id,"Текущий курс доллара США по отношению к гривне: "+str(round(dictionary.get('rate'),2)))
        elif(message.text=="EUR"):
            dictionary = finding_needed_dictionary(x, 978)
            bot.send_message(message.chat.id,"Текущий курс евро по отношению к гривне: "+str(round(dictionary.get('rate'),2)))
        else:
            bot.send_message(message.chat.id,'Спасибо за пользование!',reply_markup=types.ReplyKeyboardRemove())

# @bot.message_handler(content_types=['text'])
# def logger(message):
#     print(message.from_user.username+" "+message.from_user.first_name+" "+message.from_user.last_name+" "+str(datetime.datetime.fromtimestamp(message.date))+" "+message.text)
#     with open('messagelog.txt','w') as file:
#         file.write(message.from_user.username+" "+message.from_user.first_name+" "+message.from_user.last_name+" "+str(datetime.datetime.fromtimestamp(message.date))+" "+message.text)

        #dollar_dictionary = finding_needed_dictionary(x,840)

        #print("sent this message \n "+"Текущий курс доллара США по отношению к гривне:" +str(round(dollar_dictionary.get('rate'),2)))

        #bot.send_message(message.chat.id,"Текущий курс доллара США по отношению к гривне: "+str(round(dollar_dictionary.get('rate'),2)))



if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
                time.sleep(5)
                print("Internet error!")
