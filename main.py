"""Телеграм бот который умеет добавлять в хранилище и возвращать из него случайный мем"""
import os
import random
import telebot

token = os.environ['TELEGRAM_BOT_TOKEN']
bot_ = telebot.TeleBot(token)


@bot_.message_handler(commands=['start'], content_types=['text'])
def start(message):
    """Хэндлер приветствия пользователя"""
    text = 'Добро пожаловать в бот рандомных мемасиков!\n' \
           'Чтобы получить мем введите команду /get\n' \
           'Если хотите добавить новый мем в базу данных, просто пришлите фото'
    bot_.send_message(message.from_user.id, text)


@bot_.message_handler(commands=['help'], content_types=['text'])
def get_mem_handler(message):
    """Хэндлер который обрабатывает запрос /get возвращающий случайный мем"""
    print('Processing /get request')
    random_num = random.randint(0, len(os.listdir('memes')) - 1)
    with open(f'memes/mem{random_num}.jpg', 'rb') as send_photo:
        bot_.send_photo(message.from_user.id, photo=send_photo)


@bot_.message_handler(content_types=['photo'])
def add_mem_handler(message):
    """Хэндлер который добавляет фото присланное пользователем в хранилище"""
    print('Processing \"add new mem\" request')
    index = len(os.listdir('memes'))
    path = f'memes/mem{index}.jpg'
    file_id = message.photo[2].file_id
    file_info = bot_.get_file(file_id)
    downloaded_file = bot_.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)


def main():
    """Начало работы бота"""
    random.seed(2341)
    print('Starting bot')
    bot_.polling(none_stop=True, interval=0)


main()
