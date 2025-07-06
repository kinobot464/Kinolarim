import telebot
from telebot import types

TOKEN = '7755025869:AAFDCesSjxHP7LJxufOyJ1mzqwU4qaUNyBU'  # ← bu yerga o'zingizning tokeningizni qo'ying
bot = telebot.TeleBot(TOKEN)

# 👇 Majburiy obuna kanallar
CHANNELS = ['@kinolar_olami12346', '@AFSUNGAR_MERLIN_SERIALI_K']

# 👇 Kinolar kodi bazasi
MOVIES = {
    "1": "🎬 Kino: X odamlar\n📥 https://t.me/KINOLARtv07/1319",
    "70": "🎬 Kino: interstellir\n📥 https://t.me/KINOLARtv07/1397"
 }

# 👇 Obuna tekshiruvchi funksiya
def check_subs(user_id):
    for ch in CHANNELS:
        res = bot.get_chat_member(ch, user_id)
        if res.status not in ['member', 'administrator', 'creator']:
            return False
    return True

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for ch in CHANNELS:
        markup.add(types.InlineKeyboardButton(text=f"➕ Obuna bo‘lish: {ch}", url=f"https://t.me/{ch[1:]}"))
    markup.add(types.InlineKeyboardButton(text="✅ Tekshirish", callback_data="check"))
    bot.send_message(message.chat.id, "❗ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)

# Tekshiruv tugmasi bosilganda
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check":
        if check_subs(call.from_user.id):
            bot.send_message(call.message.chat.id, "✅ Obuna tasdiqlandi!\nEndi kino kodini yuboring:")
        else:
            bot.send_message(call.message.chat.id, "❌ Obuna topilmadi. Iltimos, barcha kanallarga obuna bo‘ling.")

# Kino kodi yuborilganda
@bot.message_handler(func=lambda message: True)
def get_movie(message):
    if check_subs(message.from_user.id):
        code = message.text.strip()
        if code in MOVIES:
            bot.send_message(message.chat.id, MOVIES[code])
        else:
            bot.send_message(message.chat.id, "❌ Bunday kod bilan kino topilmadi.")
    else:
        start(message)  # Obuna so‘rash

bot.polling()
