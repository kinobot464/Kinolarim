import telebot
import json

API_TOKEN = '8122568214:AAExyNrxhPOV1UUbMIdOL3EDKECaLq6X0lI'
bot = telebot.TeleBot(API_TOKEN)

REQUIRED_CHANNELS = ['https://t.me/AFSUNGAR_MERLIN_SERIALI_K, 'https://t.me/KINOLARtv07']

with open('data/movies.json', 'r') as f:
    movie_db = json.load(f)

def check_subscription(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_subscription(message.from_user.id):
        channels = '\\n'.join([f'➡️ {c}' for c in REQUIRED_CHANNELS])
        bot.send_message(message.chat.id, f"👋 Botdan foydalanish uchun quyidagilarga obuna bo‘ling:\\n{channels}")
    else:
        bot.send_message(message.chat.id, "✅ Obuna tekshirildi! Endi kino kodini yuboring.")

@bot.message_handler(func=lambda message: True)
def handle_code(message):
    if not check_subscription(message.from_user.id):
        channels = '\\n'.join([f'➡️ {c}' for c in REQUIRED_CHANNELS])
        bot.send_message(message.chat.id, f"❌ Iltimos, quyidagilarga obuna bo‘ling:\\n{channels}")
        return

    code = message.text.strip().lower()
    if code in movie_db:
        movie = movie_db[code]
        bot.send_message(
            message.chat.id,
            f"🎬 {movie['title']} ({movie['year']})\\n🔗 [Ko‘rish uchun]({movie['link']})",
            parse_mode='Markdown'
        )
    else:
        bot.send_message(message.chat.id, "❌ Bunday kod topilmadi.")

bot.infinity_polling()
