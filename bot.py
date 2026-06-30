from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from config import TOKEN, ADMIN_ID, SITE_URL
from database import add_user, add_order
from ai import get_ai_response

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    add_user(user.id, user.username)

    keyboard = [
        [InlineKeyboardButton("🌐 خدمات", callback_data="services")],
        [InlineKeyboardButton("📦 سفارش", callback_data="order")],
        [InlineKeyboardButton("🤖 AI مشاور", callback_data="ai")],
        [InlineKeyboardButton("🌍 سایت", url=SITE_URL)],
        [InlineKeyboardButton("📞 ارتباط با ادمین", callback_data="admin")]
    ]

    await update.message.reply_text(
        "🚀 به ANOX خوش آمدی",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "services":
        await q.edit_message_text("🌐 خدمات:\n- سایت\n- امنیت\n- ربات تلگرام")

    elif q.data == "order":
        await q.edit_message_text("📦 لطفاً اسم سرویس رو بفرست")

    elif q.data == "ai":
        await q.edit_message_text("🤖 سوالت رو بفرست")

    elif q.data == "admin":
        await q.edit_message_text("📞 پیام بده به ادمین")


# پیام‌ها
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # AI پاسخ
    ai_reply = get_ai_response(text)

    await update.message.reply_text(ai_reply)

    # ارسال به ادمین
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 از {user.username}:\n{text}"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

app.run_polling()