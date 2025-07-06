from flask import Flask, request
import telebot
import os

TOKEN = "8122568214:AAExyNrxhPOV1UUbMIdOL3EDKECaLq6X0lI"
bot = telebot.TeleBot(TOKEN)

WEBHOOK_URL = 'https://kinobot1-1-jm8r.onrender.com/'  # Renderdagi URL manzilingiz

app = Flask(__name__)

# Webhook sozlash
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '!', 200
    return 'Bot ishlayapti!', 200


# /start komandasi uchun handler
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Salom! Kino kodini yuboring.")

# Render ishga tushganda webhookni sozlash
@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

# Flask serverni ishga tushirish
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)