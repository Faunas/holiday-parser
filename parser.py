import datetime
import time

import fake_useragent
import requests
import schedule
import telebot
from bs4 import BeautifulSoup

#   print(datetime.datetime.today().weekday())
BOT_TOKEN = "TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)
chat_id_i = 1164013363


def take_day_name():
    """
    Возвращает название текущего дня недели.
    """
    weekday_names = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    weekday = datetime.datetime.today().weekday()
    day = weekday_names.get(weekday, 'Я сбился со счёту, соре')
    return day

def send_meme_for_day(path_to_photo):
    with open(path_to_photo, 'rb') as photo:
        bot.send_photo(chat_id=chat_id_i, photo=photo)

def supermemeday():
    """
    Отправляет мемасик в чат, если сегодня определенный день.
    """
    day_to_meme = {
        'Понедельник': 'Ponedelnik.jpg',
        'Вторник': 'Vtornik.jpg',
        'Среда': 'Sreda.jpg',
        'Четверг': 'Chetverg.jpg',
        'Пятница': 'URAPYATNICA.jpg',
        'Суббота': 'Subbota.jpg',
        'Воскресенье': 'Voscresenie.jpg',
    }
    day_name = take_day_name()
    if day_name in day_to_meme:
        send_meme_for_day(day_to_meme[day_name])


def take_a_holiday_day(day):
    """
    Возвращает текстовое сообщение с праздниками на сегодняшнюю дату и текущим днём недели.
    """
    now = datetime.datetime.now()
    user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': user_agent}
    url = 'https://kakoysegodnyaprazdnik.com/'
    response = requests.get(url, headers=header).content
    soup = BeautifulSoup(response, 'lxml')
    block_with_all = soup.find('ul', class_='first')
    titles = block_with_all.find_all('li', class_='block1')
    day_list = []
    for i in titles:
        day_list.append(i.text)
    message = (f'🌞Доброе утра, дЕвАчКи!✌\n'
               f'👉Сегодня {now.day}.0{now.month}.2023    ({day})\n'
               f'🥳Ваши любимые праздники:\n')
    for i, holiday in enumerate(day_list):
        message += f'- {holiday}\n'
        if i == 8:
            break

    return message


def job():
    bot.send_message(chat_id=chat_id_i, text=take_a_holiday_day(take_day_name()))
    bot.send_audio(chat_id=chat_id_i,
                   audio=open('Мама Отличника - Хи-хи, ха-ха. Вот вам и хи-хи, ха-ха, девочки!.mp3', 'rb')) \
        # Мемасики после праздников
    supermemeday()


#   job()
my_random_sleep = 1
schedule.every().day.at("07:15").do(job)

while True:
    # print(take_a_holiday_day())
    schedule.run_pending()
    time.sleep(1)
