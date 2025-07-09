import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, 
    CallbackQueryHandler, MessageHandler, Filters
)

# Configuration with your actual details
BOT_TOKEN = "8002324253:AAGaKnrU9YTp-lT-QPMLq5fG1XGFJ45siHI"
TWITTER_USERNAME = "aspen57640"
TELEGRAM_CHANNEL = "crypto_gemc"
TELEGRAM_GROUP = "pcrypto_gem"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("📣 Join Channel", url=f"https://t.me/{TELEGRAM_CHANNEL}"),
            InlineKeyboardButton("👥 Join Group", url=f"https://t.me/{TELEGRAM_GROUP}")
        ],
        [InlineKeyboardButton("🐦 Follow Twitter", url=f"https://x.com/{TWITTER_USERNAME}")],
        [InlineKeyboardButton("✅ I've Completed All Tasks", callback_data='submit')]
    ]
    
    update.message.reply_text(
        f"🌟 *WELCOME {user.first_name} TO PEAFI AIRDROP!* 🌟\n\n"
        "💰 *Claim 100 SOL Reward* 💰\n\n"
        "Complete these simple steps:\n"
        "1. Join our Telegram Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow us on Twitter\n\n"
        "Click the buttons below to complete the tasks, then press *I've Completed All Tasks*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

def handle_submission(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    # Edit original message to show completion
    query.edit_message_text(
        "🎉 *TASKS SUBMITTED! WELL DONE!*\n\n"
        "ℹ️ Hope you didn't cheat the system!\n\n"
        "Please send your Solana wallet address now.\n\n"
        "Example: `sol1xyza...`",
        parse_mode='Markdown'
    )

def handle_wallet(update: Update, context: CallbackContext) -> None:
    wallet = update.message.text.strip()
    user = update.effective_user
    
    # Send congratulations message
    update.message.reply_text(
        f"🚀 *CONGRATULATIONS {user.first_name.upper()}!* 🚀\n\n"
        "YOU PASSED PEAFI AIRDROP!\n\n"
        f"💸 *100 SOL* is on its way to your wallet:\n`{wallet}`\n\n"
        "🔸 Note: This is a test bot - no actual SOL will be sent\n"
        "🔸 Thank you for participating in our test!",
        parse_mode='Markdown'
    )
    
    # Log the submission
    logger.info(f"New submission: {user.username} | Wallet: {wallet}")

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_submission, pattern='^submit$'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))

    # Start the bot
    updater.start_polling()
    logger.info("🤖 Bot started successfully")
    logger.info(f"🔗 Bot Link: https://t.me/{updater.bot.username}")
    logger.info("⚙️ Press Ctrl+C to stop")
    updater.idle()

if __name__ == '__main__':
    main()
