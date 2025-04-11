import os
import requests
import json
import random
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
import pytz  # <- ADDED FOR TIMEZONE FIX

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = "-1002139585995"
bot = Bot(token=BOT_TOKEN)

# Random sticker list for WIN
stickers = [
    "CAACAgQAAxkBAAKmh2f5EBjXCvSqjGVYDT9P7yjKW6_IAAKOCAACi9XoU5p5sAokI77kNgQ",
    "CAACAgQAAxkBAAKmimf5EB9GTlXRtwVB3ez1nBUKzf69AAKaDAACfx_4UvcUEDj6i_r9NgQ",
    "CAACAgQAAxkBAAKmjWf5ECecZUCJtSeuqsaaVWILpTuyAALICwACG86YUDSKklgR_M5FNgQ",
    "CAACAgIAAxkBAAKmkGf5EDBgwnSDovUPpQGsTjMQdU69AAL4DAACNyx5S6FYW3VBcuj4NgQ"
]

# Get latest period number
def get_latest_period():
    url = "https://api.51gameapi.com/api/webapi/GetNoaverageEmerdList"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json",
        "Authorization": "Bearer YOUR_TOKEN_HERE"  # Replace this with valid token
    }
    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 1,
        "language": 0,
        "random": "6fadc24ccf2c4ed4afb5a1a5f84d2ba4",
        "signature": "4E071E587A80572ED6065D6F135F3ABE",
        "timestamp": 1733117040
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    try:
        data = response.json()
        return int(data["data"]["list"][0]["issueNumber"]) + 1
    except:
        return None

# Choose Big or Small randomly
def get_random_prediction():
    return random.choice(["Big", "Small"])

# Send Telegram message
def send_prediction():
    period = get_latest_period()
    if not period:
        print("Error fetching period.")
        return

    prediction = get_random_prediction()
    message = f"[WINGO 1MINUTE]\nPeriod {period}\nChoose - {prediction}"
    bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
    
    # Send WIN sticker 50% randomly (simulated win)
    if random.random() < 0.5:
        chosen_sticker = random.choice(stickers)
        bot.send_sticker(chat_id=GROUP_CHAT_ID, sticker=chosen_sticker)

    print(f"Sent: {message}")

# Schedule every 1 minute with pytz timezone fix
scheduler = BlockingScheduler(timezone=pytz.utc)
scheduler.add_job(send_prediction, 'interval', minutes=1)
scheduler.start()
