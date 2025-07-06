import telebot
from telebot import types
import requests
from flask import Flask

TOKEN = "8122568214:AAExyNrxhPOV1UUbMIdOL3EDKECaLq6X0lI"
bot = telebot.TeleBot(TOKEN)

# Flask hiyla usuli uchun
app = Flask(__name__)

# Majburiy kanal
CHANNEL_ID = "@kinolar_olami12346"  # E'tibor bering: "@" bilan yoziladi

# Kodlarga mos kinolar (qo'lda qo‘shib boriladi)
movies = {
    "70": "https://t.me/KINOLARtv07/1397",  # misol
    "72": "https://t.me/KINOLARtv07/1400",
"71": "https://t.me/KINOLARtv07/1399"
}

# Flask index sahifa
@app.route('/')
def index():
    return "Bot ishlayapti!"

# Foydalanuvchi start bosganda
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if check_subscription(user_id):
        bot.send_message(user_id, "🎬 Kino kodini yuboring:")
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("✅ Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID[1:]}")
        markup.add(btn)
        bot.send_message(user_id, "Botdan foydalanish uchun kanalga obuna bo‘ling!", reply_markup=markup)

# Kodni yozganda
@bot.message_handler(func=lambda message: True)
def send_movie(message):
    user_id = message.chat.id
    if not check_subscription(user_id):
        bot.send_message(user_id, "Avval kanalga obuna bo‘ling.")
        return

    code = message.text.strip()
    if code in movies:
        bot.send_message(user_id, f"Kino: {movies[code]}")
    else:
        bot.send_message(user_id, "❌ Bunday kod topilmadi.")

# Obuna bo‘lganligini tekshiruvchi funksiya
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# Botni Flask orqali ishga tushiramiz
import threading
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)