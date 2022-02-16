import time
from notify import Telegram
from config import config
from api import is_instance_launched, is_succeed_preparation

if __name__ == "__main__":
    tg_client = Telegram(bot_api=config.bot_api, chat_id=config.chat_id)
    tg_client.send(is_succeed_preparation())
    while True:
        if not is_instance_launched():
            time.sleep(config.wait_interval)
            continue
        break
    tg_client.send("success! go to control panel and check it!")
    tg_client.close()
