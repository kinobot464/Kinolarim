import telebot
from telebot import types
from flask import Flask
import threading
import json
import os

TOKEN = "8172792417:AAGcFzg9GjsFuGsmGpK4pUhrFSy26aZa2sk"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
ADMINS = [2097478310]

# Fayllar
os.makedirs("data", exist_ok=True)
MOVIE_FILE = "data/movies.json"
USERS_FILE = "data/users.txt"
CHANNELS_FILE = "data/channels.json"
DEFAULT_CHANNELS = [
    "@KINOLARtv07",
    "@AFSUNGAR_MERLIN_SERIALI_K",
    "@kinolar_olami12346",
    "-1002683638848",
    "https://t.me/+NPRSL0vC3_wyZTdi"
]

# Fayllarni yaratish
if not os.path.exists(MOVIE_FILE):
    with open(MOVIE_FILE, "w") as f:
        json.dump({}, f)
if not os.path.exists(USERS_FILE):
    open(USERS_FILE, "a").close()
if not os.path.exists(CHANNELS_FILE):
    with open(CHANNELS_FILE, "w") as f:
        json.dump(DEFAULT_CHANNELS, f)

def get_channels():
    with open(CHANNELS_FILE, "r") as f:
        return json.load(f)

def is_subscribed(user_id):
    for channel in get_channels():
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'creator', 'administrator']:
                return False
        except:
            return False
    return True

def save_user(user_id):
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    if is_subscribed(user_id):
        save_user(user_id)
        bot.send_message(user_id, "🎬 Kino kodini yuboring:")
    else:
        markup = types.InlineKeyboardMarkup()
        for ch in get_channels():
            btn = types.InlineKeyboardButton(f"➕ {ch}", url=f"https://t.me/{ch[1:]}")
            markup.add(btn)
        bot.send_message(user_id, "❗️Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.strip()

    if not is_subscribed(user_id):
        bot.send_message(user_id, "❗️Avval barcha majburiy kanallarga obuna bo‘ling.")
        return

    if user_id in ADMINS and text == "/panel":
        show_admin_panel(message)
        return

    if user_id in ADMINS:
        if text == "📤 Kino joylash":
            upload(message)
            return
        elif text == "📃 Kodlar ro‘yxati":
            list_codes(message)
            return
        elif text == "📢 Xabar yuborish":
            bot.send_message(user_id, "✉️ Xabar matnini kiriting:")
            bot.register_next_step_handler(message, do_broadcast)
            return
        elif text == "📡 Kanal sozlamalari":
            show_channels(message)
            return
        elif text == "⬅️ Ortga":
            show_admin_panel(message)
            return

    with open(MOVIE_FILE, "r") as f:
        movies = json.load(f)

    if text in movies:
        bot.send_video(user_id, movies[text])
    else:
        bot.send_message(user_id, "❌ Bunday kod topilmadi.")

def show_admin_panel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📤 Kino joylash", "📃 Kodlar ro‘yxati")
    markup.add("📢 Xabar yuborish", "📡 Kanal sozlamalari")
    bot.send_message(message.chat.id, "🔧 Admin panel:", reply_markup=markup)

def upload(message):
    bot.send_message(message.chat.id, "🎥 Kino faylini yuboring:")
    bot.register_next_step_handler(message, save_video)

def save_video(message):
    if message.video:
        file_id = message.video.file_id
        bot.send_message(message.chat.id, "🆔 Kino uchun kod yozing:")
        bot.register_next_step_handler(message, lambda msg: save_code(msg, file_id))
    else:
        bot.send_message(message.chat.id, "❌ Kino fayl yuborilmadi.")

def save_code(message, file_id):
    code = message.text.strip()
    with open(MOVIE_FILE, "r") as f:
        movies = json.load(f)
    movies[code] = file_id
    with open(MOVIE_FILE, "w") as f:
        json.dump(movies, f)
    bot.send_message(message.chat.id, f"✅ Kod [{code}] uchun kino saqlandi.")

def list_codes(message):
    with open(MOVIE_FILE, "r") as f:
        movies = json.load(f)
    if movies:
        txt = "\n".join([f"{k}" for k in movies.keys()])
        bot.send_message(message.chat.id, f"🎞 Kodlar:\n{txt}")
    else:
        bot.send_message(message.chat.id, "📭 Hech qanday kod yo‘q.")

def do_broadcast(message):
    text = message.text
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    count = 0
    for uid in users:
        try:
            bot.send_message(uid, text)
            count += 1
        except:
            continue
    bot.send_message(message.chat.id, f"✅ {count} foydalanuvchiga yuborildi.")

def show_channels(message):
    channels = get_channels()
    text = "📡 Majburiy kanallar:\n" + "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(channels)])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish", "⬅️ Ortga")
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "➕ Kanal qo‘shish")
def add_channel(message):
    bot.send_message(message.chat.id, "✏️ Kanalni @username ko‘rinishida yuboring:")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    ch = message.text.strip()
    if not ch.startswith("@"):
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri format.")
        return
    channels = get_channels()
    if ch in channels:
        bot.send_message(message.chat.id, "⚠️ Bu kanal allaqachon mavjud.")
    else:
        channels.append(ch)
        with open(CHANNELS_FILE, "w") as f:
            json.dump(channels, f)
        bot.send_message(message.chat.id, f"✅ {ch} qo‘shildi.")

@bot.message_handler(func=lambda m: m.text == "➖ Kanal o‘chirish")
def remove_channel(message):
    channels = get_channels()
    text = "🗑 Qaysi kanalni o‘chirasiz? Raqamini yuboring:\n" + "\n".join([f"{i+1}. {ch}" for i, ch in enumerate(channels)])
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, confirm_remove_channel)

def confirm_remove_channel(message):
    try:
        idx = int(message.text.strip()) - 1
        channels = get_channels()
        ch = channels.pop(idx)
        with open(CHANNELS_FILE, "w") as f:
            json.dump(channels, f)
        bot.send_message(message.chat.id, f"✅ {ch} o‘chirildi.")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri raqam.")

@app.route('/')
def index():
    return "Bot ishlayapti!"

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
