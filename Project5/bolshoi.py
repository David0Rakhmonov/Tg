import time
import json
import telebot
import time
from config import token

bot = telebot.TeleBot(token=token)

def get_users():
    try:
        with open('users.json') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.id
    bot.send_message(user, "Здравствуйте, этот бот будет присылать изменение афиш большого театра.")


@bot.message_handler(commands=['subscribe'])
def add_user(message):
    print(1)
    users = get_users()

    if message.chat.id not in users:
        users.append(message.chat.id)
        save_users(users)
    bot.send_message(message.chat.id, "Вы подписались на рассылку.")

@bot.message_handler(commands=['unsubscribe'])
def remove_user(message):
    users = get_users()

    if message.chat.id in users:
        users.remove(message.chat.id)
        save_users(users)
    bot.send_message(message.chat.id, "Вы отписались от рассылки.")

if __name__ == '__main__':
    bot.polling(none_stop=True)


