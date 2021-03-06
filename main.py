"""Телеграм бот, который умеет добавлять в хранилище и возвращать из него случайную картинку"""
import os
import random
import telebot

token = os.environ['TELEGRAM_BOT_TOKEN']
bot_ = telebot.TeleBot(token)


@bot_.message_handler(commands=['start'], content_types=['text'])
def start(message):
    """Хэндлер приветствия пользователя"""
    text = 'Добро пожаловать в бот рандомных картинок!\n' \
           'Чтобы получить картинку, введите команду /get\n' \
           'Если хотите добавить новый картинку в базу данных, просто пришлите фото'
    bot_.send_message(message.from_user.id, text)


@bot_.message_handler(commands=['get'], content_types=['text'])
def get_picture_handler(message):
    """Хэндлер который обрабатывает запрос /get возвращающий случайную картинку"""
    print('Processing /get request')
    dir_name = f'pictures_{message.from_user.id}'
    if dir_name in os.listdir():
        random_num = random.randint(0, len(os.listdir(dir_name)) - 1)
        with open(f'{dir_name}/p{random_num}.jpg', 'rb') as send_photo:
            bot_.send_photo(message.from_user.id, photo=send_photo)
    else:
        text = 'Хранилище пустое! Добавьте картинку'
        bot_.send_message(message.from_user.id, text)


@bot_.message_handler(content_types=['photo'])
def add_picture_handler(message):
    """Хэндлер который добавляет картинку, присланную пользователем в хранилище"""
    print('Processing \"add new picture\" request')
    dir_name = f'pictures_{message.from_user.id}'
    if dir_name not in os.listdir():
        os.mkdir(dir_name)
    index = len(os.listdir(dir_name))
    path = f'{dir_name}/p{index}.jpg'
    file_id = message.photo[2].file_id
    file_info = bot_.get_file(file_id)
    downloaded_file = bot_.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    text = 'Картинка успешно добавлена в коллекцию'
    bot_.send_message(message.from_user.id, text)


@bot_.message_handler(content_types=['text'])
def other_text_handler(message):
    """Хэндлер который обрабатывает остальные случаи"""
    print('Processing \"other text\" request')
    text = 'Я не понимаю команду.....!\n' \
           'Чтобы получить картинку введите команду /get\n' \
           'Если хотите добавить новую картинку в базу данных, просто пришлите фото'
    bot_.send_message(message.from_user.id, text)


@bot_.message_handler(content_types=['document', 'sticker', 'video', 'voice'])
def other_handler(message):
    """Хэндлер который обрабатывает остальные случаи"""
    print('Processing \"other text\" request')
    text = 'Упс, я умею работать только с картинками:('
    bot_.send_message(message.from_user.id, text)


def main():
    """Начало работы бота"""
    random.seed(2341)
    print('Starting bot')
    bot_.polling(none_stop=True, interval=0)


main()
