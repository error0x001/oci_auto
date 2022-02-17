import time
from notify import Telegram
from config import config
from api import is_instance_launched, is_succeed_preparation


def run():
    notificator = Telegram(bot_id=config.bot_id, chat_id=config.chat_id)
    ok, msg = is_succeed_preparation()
    notificator.send(msg)
    if not ok:
        exit(1)
    while True:
        if not is_instance_launched():
            time.sleep(config.wait_interval)
            continue
        break
    notificator.send("success! go to the control panel and check it!")
    notificator.close()


if __name__ == "__main__":
    run()
