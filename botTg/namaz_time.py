import telebot
import datetime
from telebot import types
import requests

bot = telebot.TeleBot('6998494909:AAFNJDcHu3XNTzf2VPxi6MpYfPTrz8Pc-cE')

city_name = ''
def write_req(mess, name):
    try:
        with open("text1.txt", "a", encoding='utf8') as file:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{now}:--{name} -- {mess}\n")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")


@bot.message_handler(commands=['start'])
def start(message):
    object1 = types.InlineKeyboardMarkup()
    btnnamaz = types.InlineKeyboardButton('Время намаза', callback_data='namaz')
    btnkubla = types.InlineKeyboardButton('Местоположение Киблы',
                                          url='https://qiblafinder.withgoogle.com/intl/ru/desktop/finder')
    object1.row(btnnamaz, btnkubla)
    btnlesson = types.InlineKeyboardButton('Научиться совершать Намаз', callback_data='lesson')
    object1.row(btnlesson)
    bot.send_message(message.chat.id, f'Ассаламу Алейкум, {message.from_user.username}', reply_markup=object1)
    print(f'{str(datetime.datetime.now())}--{message.from_user.username}')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global city_name
    object2 = types.InlineKeyboardMarkup()
    btnmoskow = types.InlineKeyboardButton('Москва', callback_data='Moskow')
    btnmakha = types.InlineKeyboardButton('Махачкала', callback_data='Makhachkala')
    btngrozni = types.InlineKeyboardButton('Грозный', callback_data='Grozniy')
    btnrostow = types.InlineKeyboardButton('Ростов-на-Дону', callback_data='Rostow')
    btnkazan = types.InlineKeyboardButton('Казань', callback_data='Kazan')
    btnvoron = types.InlineKeyboardButton('Воронеж', callback_data='Voronezh')
    btnkrasnodar = types.InlineKeyboardButton('Краснодар', callback_data='Krasnodar')
    object2.row(btnkazan, btnrostow)
    object2.row(btngrozni, btnmakha)
    object2.row(btnmoskow, btnvoron)
    object2.row(btnkrasnodar)

    if callback.data == 'namaz':
        bot.send_message(callback.message.chat.id,
                         f'Выберите город из списка, либо укажите на английском! (Makhachkala)', reply_markup=object2)
        bot.register_next_step_handler(callback.message, time)

    elif callback.data == 'lesson':
        file = open('Video/namaz.mp4', 'rb')
        bot.send_video(callback.message.chat.id, file)


def time(message):
    global city_name
    city_name = message.text

    print(f'{str(datetime.datetime.now())}--{message.from_user.username}--{city_name}')
    url = f"http://api.aladhan.com/v1/timingsByCity?city={str(city_name)}&country=Russia&method=14"
    response = requests.get(url)
    data = response.json()

    if data["code"] == 200:
        timings = data["data"]["timings"]
        prayer_times_text = (
            f"Время намаза для {city_name}:\n"
            f"Фаджр: {timings['Fajr']}\n"
            f"Восход: {timings['Sunrise']}\n"
            f"Зухр: {timings['Dhuhr']}\n"
            f"Аср: {timings['Asr']}\n"
            f"Магриб: {timings['Maghrib']}\n"
            f"Иша: {timings['Isha']}"
        )
        bot.send_message(message.chat.id, prayer_times_text)
        print('okkkk')
    else:
        bot.send_message(message.chat.id,
                         f'Извините, {message.from_user.username}, для данного города время намаза пока не доступно')
        print('ne okk')
        


@bot.message_handler(commands=['help'])
def helps(message):
    bot.send_message(message.chat.id, f'этот бот позволит: \n'
                                      f'1-узнать время намаза по России \n'
                                      f'2-определить местонахождение Киблы🕋 \n'
                                      f'3-научится совершать намаз \n')


bot.polling(none_stop=True)
