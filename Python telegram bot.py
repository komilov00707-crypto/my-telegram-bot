import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = '7359951827:AAHJbSkWUl3jK7KuL3NMvTgXB0AmatsOZQw'
ADMIN_IDS = [7214979572, 7247711357]  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Savolingizni yozing. Admin sizga alohida javob beradi.")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.full_name
    user_message = update.message.text
    
    for admin_id in ADMIN_IDS:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Javob yozish", callback_data=f"reply_to:{user_id}")]
        ])
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"📩 Yangi xabar {user_name} (ID: {user_id}):\n\n{user_message}",
            reply_markup=keyboard
        )

    await update.message.reply_text("Savolingiz yuborildi. Iltimos, javobni kuting.")

async def reply_button_clicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id not in ADMIN_IDS:
        await query.edit_message_text("Sizda javob berish huquqi yo‘q.")
        return

    data = query.data.split(":")
    if len(data) == 2 and data[0] == "reply_to":
        user_id = data[1]
        reply_command = f"/reply {user_id} Sizning javobingiz"
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=f"✏️ Quyidagi formatda javob yozing:\n\n{reply_command}",
            parse_mode="Markdown"
        )

async def handle_reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Sizda bu buyruqni ishlatish huquqi yo‘q.")
        return

    try:
        parts = update.message.text.split(maxsplit=2)
        if len(parts) < 3:
            await update.message.reply_text("To‘g‘ri format: /reply user_id javob matni")
            return

        user_id = int(parts[1])
        message = parts[2]

        await context.bot.send_message(chat_id=user_id, text=f"📬 Admin javobi:\n{message}")
        await update.message.reply_text("✅ Javob yuborildi.")

    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", handle_reply_command))
    app.add_handler(CallbackQueryHandler(reply_button_clicked, pattern="^reply_to:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("🤖 Bot ishlayapti...")
    app.run_polling()
