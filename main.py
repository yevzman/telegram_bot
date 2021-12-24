import os
import random
import telebot

token = os.environ['TELEGRAM_BOT_TOKEN']
bot_ = telebot.TeleBot(token)


@bot_.message_handler(commands=['start'], content_types=['text'])
def start(message):
    text = 'Добро пожаловать в бот рандомных мемасиков!\nЧтобы получить мем введите команду /get\nЕсли хотите добавить новый мем в базу данных, просто пришлите фото'
    bot_.send_message(message.from_user.id, text)


@bot_.message_handler(commands=['get'], content_types=['text'])
def get_mem_handler(message):
    print('Processing /get request')
    random_num = random.randint(0, len(os.listdir('memes')) - 1)
    bot_.send_photo(message.from_user.id, photo=open('memes/mem{}.jpg'.format(random_num), 'rb'))


@bot_.message_handler(content_types=['photo'])
def add_mem_handler(message):
    print('Processing \"add new mem\" request')
    path = 'memes/mem{}.jpg'.format(len(os.listdir('memes')))
    file_id = message.photo[2].file_id
    file_info = bot_.get_file(file_id)
    downloaded_file = bot_.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)


def main():
    random.seed(2341)
    print('Starting...................')
    bot_.polling(none_stop=True, interval=0)


main()
