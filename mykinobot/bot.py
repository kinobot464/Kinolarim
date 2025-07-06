from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = '8103091965:AAFtoesQh4sQcz9d7ru8EyN20DvVsnnPP8g'
CHANNELS = ['https://t.me/AFSUNGAR_MERLIN_SERIALI_K','https://t.me/kinolar_olami12346']

MOVIES = {
    '1': 'https://t.me/KINOLARtv07/1319',
    '2': 'https://t.me/KINOLARtv07/1397'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton("✅ Tekshirish", callback_data="check")]]
    text = "Quyidagi kanallarga obuna bo‘ling:\n"
    for ch in CHANNELS:
        text += f"{ch}\n"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    not_subscribed = []
    for ch in CHANNELS:
        member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
        if member.status not in ["member", "creator", "administrator"]:
            not_subscribed.append(ch)
    if not_subscribed:
        text = "Siz hali obuna bo‘lmadingiz:\n"
        for ch in not_subscribed:
            text += f"{ch}\n"
        await update.callback_query.message.reply_text(text)
    else:
        await update.callback_query.message.reply_text("✅ Obuna tasdiqlandi! Kino kodini yuboring:")

async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    if code in MOVIES:
        await update.message.reply_text(f"Kino linki: {MOVIES[code]}")
    else:
        await update.message.reply_text("❌ Kod topilmadi")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check, pattern="check"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie))

print("Bot ishga tushdi...")
app.run_polling()
