import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from openai import OpenAI

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# WARNING: Hard-coded credentials (INSECURE). Only use for quick local tests.
TELEGRAM_TOKEN = "8364249900:AAHwMq2PDpIUATHHoBsNyBgvc8GgbnMeqso"
OPENAI_API_KEY = ""

client = OpenAI(api_key=OPENAI_API_KEY)

# Simple in-memory conversation store (per chat). For production use a DB.
CONVERSATIONS = {}

SYSTEM_PROMPT = "You are a helpful AI assistant that replies in Persian (Farsi) unless the user asks otherwise."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من یک ربات هوش مصنوعی هستم. هر سوالی داری بپرس — من با کمک OpenAI جواب می‌دم."
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    CONVERSATIONS.pop(chat_id, None)
    await update.message.reply_text("چت ریست شد — حالا می‌تونی گفتگوی جدید شروع کنی.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Initialize history if needed
    history = CONVERSATIONS.setdefault(chat_id, [{"role": "system", "content": SYSTEM_PROMPT}])

    # Append user message
    history.append({"role": "user", "content": user_text})

    # Call OpenAI ChatCompletion with new API
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history,
            max_tokens=512,
            temperature=0.7,
        )
        assistant_reply = resp.choices[0].message.content.strip()
    except Exception as e:
        logger.exception("OpenAI request failed")
        await update.message.reply_text("خطا در ارتباط با سرویس هوش مصنوعی: " + str(e))
        return

    # Append assistant reply to history
    history.append({"role": "assistant", "content": assistant_reply})

    # Send reply (split if too long for Telegram)
    MAX_LEN = 4000
    if len(assistant_reply) <= MAX_LEN:
        await update.message.reply_text(assistant_reply)
    else:
        for i in range(0, len(assistant_reply), MAX_LEN):
            await update.message.reply_text(assistant_reply[i:i+MAX_LEN])

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot (long polling). This works on many PaaS, including Railway.
    logger.info("Bot starting (polling)...")
    app.run_polling()

if __name__ == "__main__":
    main()
