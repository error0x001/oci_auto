from typing import Optional

import requests
from requests import Session, RequestException

from logger import logger


class Telegram:
    __FAILED_MESSAGE = "Message fail to sent via telegram"
    __DISABLED_TELEGRAM = "[TELEGRAM BOT IS DISABLED]"

    def __init__(self, bot_api: str, chat_id: str) -> None:
        self.session: Optional[Session] = None
        self.bot_api = bot_api
        self.chat_id = chat_id
        self.__is_active = bool(self.bot_api and self.chat_id)

    def __prepare_session(self) -> None:
        self.session = requests.Session()

    def close(self) -> None:
        if not self.session:
            return
        self.session.close()

    def send(self, message: str) -> None:
        logger.info(f"{self.__DISABLED_TELEGRAM} {message}")
        if not self.__is_active:
            return
        try:
            self.session.get(
                f"https://api.telegram.org/bot{self.bot_api}/sendMessage?chat_id={self.chat_id}&text={message}"
            )
        except RequestException:
            logger.error(self.__FAILED_MESSAGE)


