import os
import logging
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Configuration with your actual details
BOT_TOKEN = "8002324253:AAGaKnrU9YTp-lT-QPMLq5fG1XGFJ45siHI"
TWITTER_USERNAME = "aspen57640"
TELEGRAM_CHANNEL = "crypto_gemc"
TELEGRAM_GROUP = "pcrypto_gem"
POLLING_INTERVAL = 1  # seconds
LAST_UPDATE_ID = 0

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    """Send a message through the Telegram Bot API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    if parse_mode:
        payload["parse_mode"] = parse_mode
    
    try:
        import requests
        response = requests.post(url, json=payload)
        return response.json()
    except ImportError:
        logger.error("Requests library not installed. Please install with: pip install requests")
        return None
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

def edit_message_text(chat_id, message_id, text, parse_mode=None):
    """Edit an existing message"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }
    
    if parse_mode:
        payload["parse_mode"] = parse_mode
    
    try:
        import requests
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Error editing message: {e}")
        return None

def answer_callback_query(callback_query_id):
    """Answer a callback query"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    payload = {
        "callback_query_id": callback_query_id
    }
    
    try:
        import requests
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Error answering callback: {e}")
        return None

def get_updates():
    """Get new updates from Telegram"""
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={LAST_UPDATE_ID + 1}&timeout=30"
    
    try:
        import requests
        response = requests.get(url)
        data = response.json()
        
        if data.get("ok") and data.get("result"):
            return data["result"]
        return []
    except Exception as e:
        logger.error(f"Error getting updates: {e}")
        return []

def handle_start(update):
    """Handle /start command"""
    user = update["message"]["from"]
    first_name = user.get("first_name", "User")
    
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📣 Join Channel", "url": f"https://t.me/{TELEGRAM_CHANNEL}"},
                {"text": "👥 Join Group", "url": f"https://t.me/{TELEGRAM_GROUP}"}
            ],
            [{"text": "🐦 Follow Twitter", "url": f"https://x.com/{TWITTER_USERNAME}"}],
            [{"text": "✅ I've Completed All Tasks", "callback_data": "submit"}]
        ]
    }
    
    message = (
        f"🌟 *WELCOME {first_name} TO PEAFI AIRDROP!* 🌟\n\n"
        "💰 *Claim 100 SOL Reward* 💰\n\n"
        "Complete these simple steps:\n"
        "1. Join our Telegram Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow us on Twitter\n\n"
        "Click the buttons below to complete the tasks, then press *I've Completed All Tasks*"
    )
    
    send_message(
        chat_id=update["message"]["chat"]["id"],
        text=message,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

def handle_submission(update):
    """Handle task submission"""
    query = update["callback_query"]
    user = query["from"]
    chat_id = query["message"]["chat"]["id"]
    message_id = query["message"]["message_id"]
    
    # Answer the callback query
    answer_callback_query(query["id"])
    
    # Edit the original message
    edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=(
            "🎉 *TASKS SUBMITTED! WELL DONE!*\n\n"
            "ℹ️ Hope you didn't cheat the system!\n\n"
            "Please send your Solana wallet address now.\n\n"
            "Example: `sol1xyza...`"
        ),
        parse_mode="Markdown"
    )

def handle_wallet(update):
    """Handle wallet submission"""
    user = update["message"]["from"]
    wallet = update["message"]["text"]
    first_name = user.get("first_name", "User")
    
    message = (
        f"🚀 *CONGRATULATIONS {first_name.upper()}!* 🚀\n\n"
        "YOU PASSED PEAFI AIRDROP!\n\n"
        f"💸 *100 SOL* is on its way to your wallet:\n`{wallet}`\n\n"
        "🔸 Note: This is a test bot - no actual SOL will be sent\n"
        "🔸 Thank you for participating in our test!"
    )
    
    send_message(
        chat_id=update["message"]["chat"]["id"],
        text=message,
        parse_mode="Markdown"
    )
    
    # Log the submission
    logger.info(f"New submission: {user.get('username', 'unknown')} | Wallet: {wallet}")

def process_updates():
    """Process incoming updates"""
    global LAST_UPDATE_ID
    
    while True:
        updates = get_updates()
        for update in updates:
            LAST_UPDATE_ID = update["update_id"]
            
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"]
                
                if text.startswith("/start"):
                    handle_start(update)
                elif "callback_query" in update:
                    # This handles the case where the message might be a callback
                    continue
                else:
                    # Handle wallet submission
                    handle_wallet(update)
            
            elif "callback_query" in update:
                handle_submission(update)
        
        time.sleep(POLLING_INTERVAL)

def start_polling():
    """Start the polling thread"""
    logger.info("🤖 Starting bot polling...")
    polling_thread = threading.Thread(target=process_updates)
    polling_thread.daemon = True
    polling_thread.start()
    logger.info("🔍 Polling for updates...")

# Health check server for Render.com
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

def run_health_server():
    """Run a simple HTTP server for health checks"""
    server_address = ('', int(os.environ.get('PORT', 10000)))
    httpd = HTTPServer(server_address, HealthCheckHandler)
    logger.info(f"🩺 Health check server running on port {server_address[1]}")
    httpd.serve_forever()

if __name__ == '__main__':
    # Start health check server in a separate thread
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()
    
    # Start the Telegram bot
    start_polling()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped")
