from flask import Flask
from threading import Thread
import telebot

TOKEN = "8122568214:AAExyNrxhPOV1UUbMIdOL3EDKECaLq6X0lI"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bu yerga bot handlerlaringizni yozasiz
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Kino kodini yuboring.")

# Polling orqali ishga tushirish
if __name__ == "__main__":
    keep_alive()
    bot.polling()